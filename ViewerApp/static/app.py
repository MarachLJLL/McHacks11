from flask import Flask, render_template, request, redirect, session, json, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from classes import db, User
from dataExtraction import getDevices
from graphing import Graph
import os
from zipfile import ZipFile
import io



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  
db.init_app(app)
app.secret_key = 'ilsr' 
app.config['SESSION_TYPE'] = 'filesystem'

with app.app_context():
    @app.route('/')
    def index():
        logged_in = session.get('logged_in', False)
        if logged_in:
            g = Graph(session["name"])
            graph_html = g.kwh_g

            return render_template('result.html', graph_html=graph_html, g = g)
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
     
            g = Graph(session["name"])
            graph_html = g.kwh_g

            return render_template('result.html', graph_html=graph_html, g = g)
        else:
            error = "Username already exists please try again."
            return render_template("index.html", error = error)
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
                g = Graph(session["name"])
                graph_html = g.kwh_g

                return render_template('result.html', graph_html=graph_html, g = g)
            else:
                error = "Invalid username or password. Please try again."
                return render_template('index.html', error=error)

        return render_template('login.html')
    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        session.pop('name', None)
        return "Logged out, session ended."

    @app.route("/create-dp", methods=["POST", "GET"])
    def create_dp():
        # if request.method == "POST":
        data = request.get_json()
        name = data['user']
        time = data['time']
        energy = data['energy']
        killed = data['killed']
        cost = data['cost']
        device_id = data['device_id']
        
        users = User.query.all()
        for user in users:
            if user.name == name and user.time == time:
                print('datapoint found already')
                return '', 201

        new_user = User(name=name, device_id=device_id, time=time,
                        energy=energy, trees_killed=killed, cost=cost)

        # Add the new user to the database
        db.session.add(new_user)
        print("added user!")
        db.session.commit()
        return redirect("graphing.html")
        
    
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
    @app.route("/graph")
    def graph():
        g = Graph(session["name"])
        graph_html = g.kwh_g
        return render_template('graphing.html', graph_html=graph_html, g = g)
    
    @app.route("/stats")
    def stats():
        g = Graph(session["name"])
        return render_template("/stats.html", g = g)

    @app.route("/show")
    def route():
        users = User.query.all()
        return render_template("/show.html", users = users)

    @app.route("/download_page")
    def download_page():
        return render_template("downloadPage.html")

    @app.route("/download")
    def download_file():
        directory_path = 'C:\\Users\\llimge\\Documents\\Mcgill Classes\\McHA 024\\McHacks11\\SenderApp'  # Path to your folder
        memory_file = io.BytesIO()

        with ZipFile(memory_file, 'w') as zf:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    filepath = os.path.join(root, file)
                    zf.write(filepath, os.path.relpath(filepath, directory_path))
        memory_file.seek(0)

        # Set the proper headers and MIME type for a zip file download
        response = send_file(memory_file, mimetype='application/zip', as_attachment=True, download_name='SenderApp.zip')
        return response

    @app.route("/result")
    def result():
        g = Graph(session["name"])
        return render_template('result.html', g = g)

    if __name__ == '__main__':
            db.create_all() 
            app.run(debug=True)
    
    