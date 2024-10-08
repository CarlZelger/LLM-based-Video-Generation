from typing import Dict, List
import requests
from pexels_api import API
  
def generateImages(topic: str, titles: List[str]) -> Dict[str, str]:
    PEXELS_API_KEY = 'PEXELS_API_KEY'
    api = API(PEXELS_API_KEY)
    ret = {}
    i=0
    searchTerm = topic
    api.search(searchTerm, page=1, results_per_page=len(titles))
    photos = api.get_entries()
    for photo in photos:
        response = requests.get(photo.landscape)
        image_path = f"image{i}.jpeg"
        with open(image_path, "wb") as file:
            file.write(response.content)
        ret[titles[i]] = image_path
        i += 1
            
    return ret

     



