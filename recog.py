import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from googlesearch import search

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
# file_name = 'images/0x0.jpeg'

def get_recipe(file_name):
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.web_detection(image=image)
    annotations = response.web_detection

    search_term = annotations.best_guess_labels[0].label

    try:
        result =  next(search("site:taste.com.au {}".format(search_term), tld="co.in", num=1, stop=1, pause=1))
        return result
    except:
        response = client.label_detection(image=image)
        labels = response.label_annotations
        for label in labels:
            try:
                result =  next(search("site:taste.com.au {}".format(search_term), tld="co.in", num=1, stop=1, pause=1))
                return result
            except:
                continue
    return None