import requests
import json
from key import key
import random

def get_image(search_item):
    url = f"https://pixabay.com/api/?key={key}&q={search_item}"
    r = requests.get(url)
    json_data = r.json()
    urls_list = []
    for image in json_data['hits']:
        url = image['largeImageURL']
        urls_list.append(url)
        # r = requests.get(url,stream=True)
    return urls_list


