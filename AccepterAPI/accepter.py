from flask import Flask, request, jsonify
from classes import db, User

app = Flask(__name__)


'''
@app.route("/")
def home():
    return "Home"
'''

@app.route("/get-user/<uid>")
def get_user(uid):
    user_data = {
        "uid": uid,
        "name": "John",
        "email": "John Cena"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra
    return jsonify(user_data), 201



@app.route("/create-dp", methods=["POST"])
def create_dp():
    # if request.method == "POST":
    data = request.get_json()
        
    # implement adding the data into the database
    print(data)
    
    return jsonify(data), 201

if __name__ == "__main__":
    app.run(debug=True)