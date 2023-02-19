import os, io
import base64
import cv2
from google.cloud import vision

def create_google_vision_client():
    os.environ['SERVICE_ACCOUNT_TOKEN'] = r'Service_Account_Token.json'
    client = vision.ImageAnnotatorClient()
    return client 

def get_text_in_image(b64_image):
    client = create_google_vision_client()

    image = vision.Image(content=b64_image) 
    response = client.text_detection(image=image) 
    texts = response.text_annotations # all identified text and related metadata 
    
    return texts

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
                endY = text.bounding_poly.vertices[3].y
                rect = (startX, startY, endX, endY) # create box

                # draw box 
                output = original_image.copy()
                output = draw_ocr_results(output, rect)
                final_image = draw_ocr_results(final_image, rect)

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



# #image locally
# IMAGE_NAME = 'doritos.jpg'
# IMAGE_PATH = '/Users/jonathanfong/Desktop/H4HAllergy_Backend/'
# with io.open(os.path.join(IMAGE_PATH, IMAGE_NAME), 'rb') as image_file:
#     image_content = image_file.read()
# b64_encoded_image = base64.b64encode(image_content).decode('utf-8')
# # print("encoded image: ", b64_encoded_image)
# image = vision.Image(content=b64_encoded_image)

# #identify text
# response = client.text_detection(image=image)
# texts = response.text_annotations

# #editing image
# decoded_image = base64.b64decode(b64_encoded_image) #decode base64 representation of image

# if os.path.exists('original_image.jpg'):
#     os.remove('original_image.jpg')

# image_to_edit = open('original_image.jpg', 'wb') 
# image_to_edit.write(decoded_image) #create image file using decoded information 

# #edit image using cv
# original_image = cv2.imread('original_image.jpg')
# # print('original_image: ', original_image)
# final = original_image.copy()

# foundAllergy = False
# allergyList = set()
# # Add relevant texts to 
# for text in texts:
#     # print(text.description)
#     for allergy in allergy_list:
#         if allergy.lower() in text.description.lower():
#             foundAllergy = True
#             allergyList.add(allergy.lower())

#             ocr = text.description
#             # print('orc: ', ocr)
#             print(text.bounding_poly.vertices)
#             startX = text.bounding_poly.vertices[0].x
#             startY = text.bounding_poly.vertices[0].y
#             endX = text.bounding_poly.vertices[1].x
#             endY = text.bounding_poly.vertices[3].y
#             rect = (startX, startY, endX, endY)
#             # print("rect coordinates: ", rect)
            
#             output = original_image.copy()
#             output = draw_ocr_results(output, ocr, rect)
#             final = draw_ocr_results(final, ocr, rect)

# # create final image
# cv2.imwrite('final_image.jpg', final)
# with open('final_image.jpg', 'rb') as final_image:
#     final_image_content = final_image.read()
# b64_encoded_final_image_data = base64.b64encode(final_image_content).decode('utf-8')
# # print("b64_encoded_final_image_data: ", b64_encoded_final_image_data)


# # show the final output image
# # cv2.imshow("Final Output", original_image)
# cv2.imshow("Final Output", final)
# cv2.waitKey(0)


# response = {}
# response['foundAllergy'] = foundAllergy
# response['allergyList'] = allergyList
# print("response: ", response)

# def main():
#     print('testing')


# if __name__ == "__main__":
#     main()
