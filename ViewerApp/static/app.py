from flask import Flask, render_template, request, redirect, session, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from classes import db, User
import jsonify
from dataExtraction import getDevices
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  
db.init_app(app)
app.secret_key = 'ilsr' 

with app.app_context():
    @app.route('/')
    def index():
        logged_in = session.get('logged_in', False)
        if logged_in:
            users = User.query.all()
            return render_template('index.html', users = users)
        else:
            return render_template('index.html')

    @app.route('/signup')
    def signup():
        return render_template('signup.html')
    @app.route('/process', methods=['POST'])
    def process():
        name = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()
        if not user:
            new_user = User(name=name, password=password)
            db.session.add(new_user)
            db.session.commit()

            session['name'] = name
            session['logged_in'] = True
     
            users = User.query.all()
            return render_template("users.html", username = name, users = users)
        else:
            error = "Username already exists please try again."
            return render_template("signup.html", error = error)
    @app.route('/login-app', methods=['GET', 'POST'])
    def verify():
        
        username = request.args.get("username")
        password = request.args.get("password")
        user = User.query.filter_by(name=username, password=password).first()
        if user:
            return '', 200
        else: 
            return '', 201

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(name=username, password=password).first()
            if user:
                session['name'] = username
                session['logged_in'] = True
                return render_template('index.html', username = session['name'])
            else:
                error = "Invalid username or password. Please try again."
                return render_template('login.html', error=error)

        return render_template('login.html')
    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        session.pop('name', None)
        return "Logged out, session ended."

    @app.route("/create-dp", methods=["POST"])
    def create_dp():
        # if request.method == "POST":
        data = request.get_json()

        return '', 201
    
    @app.route("/create")
    def create():
        return render_template("createUser.html")
    @app.route("/submit", methods = ["GET", "POST"])
    def submit():
        name = request.form['name']
        password = request.form['password']
        device_id = request.form['device_id']
        time = request.form['time']
        energy = float(request.form['energy'])
        trees_killed = int(request.form['trees_killed'])
        cost = float(request.form['cost'])

        # Create a new User instance
        new_user = User(name=name, password=password, device_id=device_id, time=time,
                        energy=energy, trees_killed=trees_killed, cost=cost)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
  
        return render_template("users.html")
    if __name__ == '__main__':
            db.create_all() 
            app.run(debug=True)