import requests
import json
import datetime
from time import sleep
from config import USER_NAME, API_KEY, MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from config import TIMESTAMP, logger, LOAD_MORE_ITEMS_COUNT
from utils.utility_functions import flatten_custom_data
from utils.mongo_db_utility import MongoDBUtility

#########################################################################################
username = USER_NAME
apiKey = API_KEY
scraper = 'facebookProfile'
url = 'https://www.facebook.com/EsteeLauder/'
 
apiEndPoint = "http://api.scraping-bot.io/scrape/data-scraper"
apiEndPointResponse = "http://api.scraping-bot.io/scrape/data-scraper-response?"

file_path = f"./data/facebook_scraped_data__{TIMESTAMP}__{LOAD_MORE_ITEMS_COUNT}_items.json"
flatten_file_path = f"./data/facebook_scraped_data__{TIMESTAMP}__{LOAD_MORE_ITEMS_COUNT}_flatten_items.json"

payload = json.dumps({"url": url, "scraper": scraper, "load_more_items_count": LOAD_MORE_ITEMS_COUNT})

headers = {
    'Content-Type': "application/json"
}

##########################################################################################

logger.info("Connecting to MongoDB")
mongoDBUtility = MongoDBUtility(MONGO_URI, DATABASE_NAME)

logger.info("Creating database")
mongoDBUtility.create_database()

logger.info("Sending request to scraping-bot.io")
response = requests.request("POST", apiEndPoint, data=payload, auth=(username, apiKey), headers=headers)
if response.status_code == 200:
    logger.info(response.json())
    logger.info(response.json()["responseId"])
    responseId = response.json()["responseId"]

    pending = True
    while pending:
        # sleep 5s between each loop, social-media scraping can take quite long to complete
        # so there is no point calling the api quickly as we will return an error if you do so
        sleep(5)
        finalResponse = requests.request("GET", apiEndPointResponse + "scraper=" + scraper + "&responseId=" + responseId
                                         , auth=(username, apiKey))
        
        result = finalResponse.json()


        if type(result) is list:
            pending = False
            logger.info(finalResponse.text)
            final_result = flatten_custom_data(result)
        
            logger.info("Writing json data to file: " + file_path)
            with open(file_path, "w") as json_file:
                json.dump(result, json_file, indent=4)
            
            logger.info("Writing flatten json data to file: " + flatten_file_path)
            with open(flatten_file_path, "w") as json_file:
                json.dump(final_result, json_file, indent=4)

            logger.info("Inserting many records of data to MongoDB")
            mongoDBUtility.insert_many_records(COLLECTION_NAME, final_result)
            
            logger.info("Closing MongoDB connection")
            mongoDBUtility.close_connection()

        elif type(result) is dict:
            if "status" in result and result["status"] == "pending":
                logger.info(result["message"])
                continue
            elif result["error"] is not None:
                pending = False
                logger.error(result["error"])

else:
    logger.info(response.text)


############################################################################################
