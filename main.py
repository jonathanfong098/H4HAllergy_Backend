from flask import Flask,jsonify,request
  
app =   Flask(__name__)

@app.route('/find-allergens-in-image', methods = ['POST'])
def find_allergens():
    request_data = request.get_json()
    print(request_data)

    user_id = request_data['userID']
    base64_image = request_data['image']

    # Get Database from Firebase
    allergies = ['salt', 'cheese', 'canola', 'onion']    

    data = {
        "userID" : user_id + "0x1234",
        "image" : base64_image + "doritos",
    }
    
    return jsonify(data)
  
if __name__=='__main__':
    app.run(debug=True)