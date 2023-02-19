import os, io
import base64
import cv2
from google.cloud import vision

def create_google_vision_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Service_Account_Token.json'
    client = vision.ImageAnnotatorClient()
    return client 

def get_text_in_image(b64_image):
    client = create_google_vision_client()

    image = vision.Image(content=b64_image) 
    response = client.text_detection(image=image) 
    texts = response.text_annotations # all identified text and related metadata 
    
    return texts

def create_detected_allergen_list(texts, allergies):

    has_allergen = False
    allergens = set()

    for text in texts:
        item = text.description.lower()
        if item in allergies:
                has_allergen = True
                allergens.add(item)

    allergens = list(allergens)
    
    return {'hasAllergen': has_allergen, 'allergens': allergens}

def create_image_with_markers(b64_image, texts, allergies):
    decode_original_image = base64.b64decode(b64_image) #decode base64 representation of image

    image_to_edit = open('original_image.jpg', 'wb') 
    image_to_edit.write(decode_original_image) #create image file using decoded information 

    original_image = cv2.imread('original_image.jpg')
    final_image = original_image.copy()

    for text in texts:
        for allergy in allergies:
            if allergy.lower() in text.description.lower():

                # get box coordinates 
                startX = text.bounding_poly.vertices[0].x
                startY = text.bounding_poly.vertices[0].y
                endX = text.bounding_poly.vertices[1].x
                endY = text.bounding_poly.vertices[2].y
                rect = (startX, startY, endX, endY) # create box

                # draw box 
                output = original_image.copy()
                output = draw_ocr_results(output, rect)
                final_image = draw_ocr_results(final_image, rect)

    # create final image with markers
    cv2.imwrite('final_image.jpg', final_image)
    with open('final_image.jpg', 'rb') as final_image_file:
        final_image_content = final_image_file.read()
    b64_final_image = base64.b64encode(final_image_content).decode('utf-8')

    # delete images 
    if os.path.exists('original_image.jpg'):
        os.remove('original_image.jpg')
    
    if os.path.exists('final_image.jpg'):
        os.remove('final_image.jpg')

    return b64_final_image


def draw_ocr_results(image, rect, color=(0,0,255)):
    # unpacking the bounding box rectangle and draw a bounding box
    # surrounding the text along with the OCR'd text itself
    (startX, startY, endX, endY) = rect
    cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
    return image

