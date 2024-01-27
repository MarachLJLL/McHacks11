from flask import Flask, request, jsonify
from classes import db, Device, EnergyConsumption, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  
db.init_app(app)
app.secret_key = 'ilsr' 

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

@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    return 200
# if not valid return 201 code
    

@app.route("/create-dp", methods=["POST"])
def create_dp():
    # if request.method == "POST":
    data = request.get_json()
        
    # implement adding the data into the database
    print(data)
    
    return jsonify(data), 201

if __name__ == "__main__":
    app.run(debug=True)