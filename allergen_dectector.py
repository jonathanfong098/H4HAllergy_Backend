import os
import cv2
from google.cloud import vision
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin
cred = credentials.Certificate("./firebase_account_key.json")
firebase_admin.initialize_app(cred)

# Get Database from Firebase
UID = 'TEMPORARY_ID'
ref = db.reference("TEMPORARY_DATABASENAME")
allergy_list = ref.get()[UID]

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Service_Account_Token.json'

#client
client = vision.ImageAnnotatorClient()

#image in the cloud
image = vision.Image()
image.source.image_uri = 'https://storage.googleapis.com/h4h_allergy/IMG_3179.jpg'

#identify text in the cloud 
response = client.text_detection(image=image)
texts = response.text_annotations
print('Texts:')

for text in texts:
    print(text.description)
    # if text.description == 'corn':
    #     print('\n"{}"'.format(text.description))

    # vertices = (['({},{})'.format(vertex.x, vertex.y)
    #             for vertex in text.bounding_poly.vertices])

    # print('bounds: {}'.format(','.join(vertices)))

if response.error.message:
    raise Exception(
        '{}\nFor more info on error messages, check: '
        'https://cloud.google.com/apis/design/errors'.format(
            response.error.message))

#file
# FILE_NAME = 'doritos.jpg'


# def draw_ocr_results(image, text, rect, color=(0, 255, 0)):
#     # unpacking the bounding box rectangle and draw a bounding box
#     # surrounding the text along with the OCR'd text itself
#     (startX, startY, endX, endY) = rect
#     cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
#     cv2.putText(image, text, (startX, startY - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
#     # return the output image
#     return image

def main():
    print('testing')


if __name__ == "__main__":
    main()
