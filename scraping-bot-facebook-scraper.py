import requests
import json
from time import sleep
from config import USER_NAME, API_KEY



username = USER_NAME
apiKey = API_KEY
scraper = 'facebookProfile'
url = 'https://www.facebook.com/EsteeLauder/'
 
apiEndPoint = "http://api.scraping-bot.io/scrape/data-scraper"
apiEndPointResponse = "http://api.scraping-bot.io/scrape/data-scraper-response?"

payload = json.dumps({"url": url, "scraper": scraper})
headers = {
    'Content-Type': "application/json"
}

response = requests.request("POST", apiEndPoint, data=payload, auth=(username, apiKey), headers=headers)
if response.status_code == 200:
    print(response.json())
    print(response.json()["responseId"])
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
            print(finalResponse.text)
            '''
            print(type(finalResponse.text))
            json_data = json.dumps(finalResponse.text, indent=4)
            print(json_data)
            with open("facebook_scrape_data.json", "w") as json_file:
                json_file.write(json_data, indent=4)
            '''
            
            
        elif type(result) is dict:
            if "status" in result and result["status"] == "pending":
                print(result["message"])
                continue
            elif result["error"] is not None:
                pending = False
                print(json.dumps(result, indent=4),frame.f_lineno)

else:
    print(response.text)