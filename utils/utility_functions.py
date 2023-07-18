from config import logger, MONGO_URI, DATABASE_NAME
from utils.mongo_db_utility import MongoDBUtility


def flatten_custom_data(dataList):
    logger.info("flatten_custom_data() called")
    flattened_data = []
    for data in dataList:
        exclude_key = "post_info"
        filtered_data = {key: value for key, value in data.items() if key != exclude_key}
        for post_info in data["post_info"]:
            post_info.update(filtered_data)
            flattened_data.append(post_info)
    logger.info("flattened_data size: " + str(len(flattened_data)))
    logger.info("flatten_custom_data() completed")
    return flattened_data


def clear_mongo_collection(collection_name):
    logger.info("clear_mongo_collection() called")
    MongoDBUtility = MongoDBUtility(MONGO_URI, DATABASE_NAME)
    MongoDBUtility.clear_collection(collection_name)
    logger.info("clear_mongo_collection() completed")
    MongoDBUtility.close_connection()
    logger.info("MongoDBUtility connection closed")



