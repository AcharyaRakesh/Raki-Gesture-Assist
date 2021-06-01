import os, io
from google.cloud import vision

# from google.cloud.vision import types
# import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'vision.json'
client = vision.ImageAnnotatorClient()


# FOLDER_PATH = r'<Folder Path>'
# IMAGE_FILE = '<image file name>'
# FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

# with io.open(FILE_PATH, 'rb') as image_file:
#    content = image_file.read()

def textimg(img_name):
    with io.open(img_name, 'rb') as image_file:
        content = image_file.read()
        # content = img_name.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)

        docText = response.full_text_annotation.text
        return (docText)
