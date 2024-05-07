from google_images_search import GoogleImagesSearch
from dotenv import load_dotenv
import os

load_dotenv()

def get_pizza_ilustration(flavor):
    gis = GoogleImagesSearch(os.getenv("search_api_key"), os.getenv("search_id"))
    
    search_params = {
        "q": f'{flavor} pizza',
        "num": 1,
        "safe": "high",
        "fileType": "jpg|png",
        "imgType": "photo"
    }
    
    gis.search(search_params=search_params)
    result = gis.results()[0]
    return result.url
