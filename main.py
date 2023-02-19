from flask import Flask,jsonify,request
from allergen_dectector import *

app =   Flask(__name__)

@app.route('/find-allergens-in-image', methods = ['POST'])
def find_allergens():
    request_data = request.get_json()
    print(request_data)

    user_id = request_data['userID']
    b64_image = request_data['image']

    # Get Database from Firebase
    allergies = ['salt', 'cheese', 'canola', 'onion']    

    # data = {
    #     "userID" : user_id + "0x1234",
    #     "image" : b64_image + "doritos",
    # }
    
    texts = get_text_in_image(b64_image)
    data = create_detected_allergen_list(texts, allergies)
    b64_image_with_markers = create_image_with_markers(b64_image, texts, allergies)
    data['image'] = b64_image_with_markers
    
    return jsonify(data)
  
if __name__=='__main__':
    app.run(debug=True)