import io
import os

# Imports the Google Cloud client library
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = 'images/web_dim-sim-sausage-rolls-169050-1.jpeg'

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.web_detection(image=image)
annotations = response.web_detection

print(annotations.best_guess_labels[0].label)