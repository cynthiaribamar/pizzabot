from google_images_search import GoogleImagesSearch
from dotenv import load_dotenv
import os
from PIL import Image
import requests

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
    results = gis.results()
    if results:
        result = results[0]
        img_url = result.url
        response = requests.get(img_url, stream=True)
        
        if response.status_code == 200:
            img = Image.open(response.raw)
            return img
        else:
            print("Failed to download image.")
    else:
        print("No results found.")
