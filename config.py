import logging
import datetime

TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

logging.basicConfig(filename=f'./logs/Facebook_Scraping_Code_{TIMESTAMP}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


USER_NAME = 'ravikb'
API_KEY = 'yukdDrHCjz1cQl5yiQxySauns'

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "Facebook_Data"
COLLECTION_NAME = "EsteeLauder"

LOAD_MORE_ITEMS_COUNT = 50 ## get the latest 50 posts
