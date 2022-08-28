import io
import os
from time import sleep

# Imports the Google Cloud client library
from google.cloud import vision
from googlesearch import search

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"

# Instantiates a client
client = vision.ImageAnnotatorClient()

def get_recipe(file_name):
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.web_detection(image=image)
    annotations = response.web_detection

    try:
        search_term = annotations.best_guess_labels[0].label
    except:
        return "Bad File"
    result = "Not Found"
    
    try:
        result = list(search("site:taste.com.au/recipes {}".format(search_term), tld="co.in", num=10, stop=10, pause=1))
        result = [item for item in result if "taste.com.au/recipes/collections" not in item][0]
    except:
        response = client.label_detection(image=image)
        labels = response.label_annotations
        for label in labels:
            try:
                print(label.description)
                result = list(search("site:taste.com.au/recipes {}".format(label.description), tld="co.in", num=5, stop=5, pause=1))
                print(result)
                result = [item for item in result if "taste.com.au/recipes/collections" not in item][0]
                return "Searched for recipe for {}.\nRecipe: {}".format(label.description, result)
            except:
                continue
    return "Searched for recipe for {}.\nRecipe: {}".format(search_term, result)