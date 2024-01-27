from flask import Flask, request, jsonify

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


    



if __name__ == "__main__":
    app.run(debug=True)