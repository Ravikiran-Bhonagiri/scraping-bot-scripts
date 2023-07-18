import pymongo
from config import logger

class MongoDBUtility:
    def __init__(self, mongo_uri, database_name):
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.client = pymongo.MongoClient(mongo_uri)

    def close_connection(self):
        self.client.close()

    def create_database(self):
        try:
            db_list = self.client.list_database_names()
            if self.database_name not in db_list:
                db = self.client[self.database_name]
                logger.info(f"Database '{self.database_name}' created successfully!")
            else:
                logger.info(f"Database '{self.database_name}' already exists.")
        except pymongo.errors.PyMongoError as e:
            logger.error("Error:", e)

    def insert_single_record(self, collection_name, record):
        try:
            db = self.client[self.database_name]
            collection = db[collection_name]
            result = collection.insert_one(record)
            logger.info("Inserted document ID: ", result.inserted_id)
        except pymongo.errors.PyMongoError as e:
            logger.error("Error:", e)

    def insert_many_records(self, collection_name, records):
        try:
            db = self.client[self.database_name]
            collection = db[collection_name]
            result = collection.insert_many(records)
            logger.info("Inserted document IDs: ", result.inserted_ids)
        except pymongo.errors.PyMongoError as e:
            logger.error("Error:", e)

    def delete_records(self, collection_name, filter_query):
        try:
            db = self.client[self.database_name]
            collection = db[collection_name]
            result = collection.delete_many(filter_query)
            logger.info(f"{result.deleted_count} document(s) deleted.")
        except pymongo.errors.PyMongoError as e:
            logger.error("Error:", e)

    def update_record(self, collection_name, filter_query, update_data):
        try:
            db = self.client[self.database_name]
            collection = db[collection_name]
            result = collection.update_one(filter_query, {"$set": update_data})
            logger.info(f"{result.modified_count} document(s) updated.")
        except pymongo.errors.PyMongoError as e:
            logger.error("Error:", e)

    def clear_collection(self, collection_name):
        try:
            db = self.client[self.database_name]
            collection = db[collection_name]
            collection.drop()
            logger.info(f"Collection '{collection_name}' cleared.")
        except pymongo.errors.PyMongoError as e:
            logger.error("Error:", e)