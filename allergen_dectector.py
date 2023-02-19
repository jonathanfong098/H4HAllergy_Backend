import os, io
import cv2
from google.cloud import vision
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin
cred = credentials.Certificate("./firebase_account_key.json")
firebase_admin.initialize_app(cred)

# Get Database from Firebase
# UID = 'TEMPORARY_ID'
# ref = db.reference('TEMPORARY_DATABASENAME')
# allergy_list = ref.get()[UID]
allergy_list = ['nuts', 'gluten', 'canola']

# draw boxes
def draw_ocr_results(image, text, rect, color=(0,0,255)):
    # unpacking the bounding box rectangle and draw a bounding box
    # surrounding the text along with the OCR'd text itself
    (startX, startY, endX, endY) = rect
    cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
    # cv2.putText(image, text, (startX, startY - 10),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    # return the output image
    return image

# client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Service_Account_Token.json'

# Client
client = vision.ImageAnnotatorClient()

#image in the cloud
#image = vision.Image()
#image.source.image_uri = 'https://storage.googleapis.com/h4h_allergy/IMG_3179.jpg'

#image locally
IMAGE_NAME = 'doritos.jpg'
IMAGE_PATH = '/Users/jonathanfong/Desktop/H4HAllergy_Backend/'
FULL_PATH = IMAGE_PATH + IMAGE_NAME
with io.open(os.path.join(IMAGE_PATH, IMAGE_NAME), 'rb') as image_file:
    content = image_file.read()
image = vision.Image(content=content)

#identify text
response = client.text_detection(image=image)
if response.error.message:
    raise Exception(
        '{}\nFor more info on error messages, check: '
        'https://cloud.google.com/apis/design/errors'.format(
            response.error.message))
texts = response.text_annotations

#editing image
cv2_image = cv2.imread(FULL_PATH)
final = cv2_image.copy()
# print('cv2_image: ', cv2_image)

#print text

foundAllergy = False
allergyList = []
# Add relevant texts to 
for text in texts:
    for allergy in allergy_list:
        if allergy.lower() in text.description.lower():
            foundAllergy = True
            allergyList.append(allergy.lower())

            ocr = text.description
            startX = text.bounding_poly.vertices[0].x
            startY = text.bounding_poly.vertices[0].y
            endX = text.bounding_poly.vertices[1].x
            endY = text.bounding_poly.vertices[2].y
            rect = (startX, startY, endX, endY)
            print("rect coordinates: ", rect)
            
            output = cv2_image.copy()
            output = draw_ocr_results(output, ocr, rect)
            final = draw_ocr_results(final, ocr, rect)
            print(ocr)

# show the final output image
cv2.imshow("Final Output", final)
cv2.waitKey(0)

    # vertices = (['({},{})'.format(vertex.x, vertex.y)
    #             for vertex in text.bounding_poly.vertices])

    # print('bounds: {}'.format(','.join(vertices)))

response = {}
response['foundAllergy'] = foundAllergy
response['allergyList'] = allergyList


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
