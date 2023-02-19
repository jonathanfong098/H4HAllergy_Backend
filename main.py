from flask import Flask,jsonify,request
from allergen_dectector import *

from firebase.firebase import *
from firebase.user import *

app = Flask(__name__)

@app.route('/find-allergens-in-image', methods = ['POST'])
def find_allergens():
    request_data = request.get_json()
    # print(request_data)

    user_id = request_data['userID']
    b64_image = request_data['image']

    # Get Database from Firebase   
    db = initialize_db()
    allergies = get_allergies(db, user_id)
    # print("allergies: ", allergies)

    data = {"allergens": [], "hasAllergen": False, "image": None}
    if allergies: 
        texts = get_text_in_image(b64_image)
        data = create_detected_allergen_list(texts, allergies)
        b64_image_with_markers = create_image_with_markers(b64_image, texts, allergies)
        data['image'] = b64_image_with_markers
    
    return jsonify(data)
  
if __name__=='__main__':
    app.run(debug=True)