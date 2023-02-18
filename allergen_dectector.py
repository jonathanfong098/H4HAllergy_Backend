# import os
import cv2
from google.cloud import vision

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Service_Account_Token'

# client = vision.ImageAnnotatorClient()




def draw_ocr_results(image, text, rect, color=(0, 255, 0)):
    # unpacking the bounding box rectangle and draw a bounding box
    # surrounding the text along with the OCR'd text itself
    (startX, startY, endX, endY) = rect
    cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
    cv2.putText(image, text, (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    # return the output image
    return image


def main():
    print('testing')


if __name__ == "__main__":
    main()
