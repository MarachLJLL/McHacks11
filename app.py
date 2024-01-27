from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database file
db = SQLAlchemy(app)

app.secret_key = 'luisisaacnazrup' #Session key
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Initialize column in database for id
    name = db.Column(db.String(100)) # Initialize column in database for name
    password = db.Column(db.String(100)) # Initialize column in databasefor password
    email = db.Column(db.String(100))


with app.app_context():
    @app.route('/')
    def index():
        return render_template('index.html')
if __name__ == '__main__':
        db.create_all()  # Create tables based on defined models
        app.run(debug=True)