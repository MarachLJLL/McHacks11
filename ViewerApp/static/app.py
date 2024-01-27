from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  
db = SQLAlchemy(app)

app.secret_key = 'ilsr' 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100)) 


with app.app_context():
    @app.route('/')
    def index():
        return render_template('index.html')
    @app.route('/signup')
    def signup():
        return render_template('signup.html')
    @app.route('/process', methods=['POST'])
    def process():
        name = request.form['username']
        password = request.form['password']
        # Check if the user is in the database already
        user = User.query.filter_by(name=name).first()
        if not user:
            new_user = User(name=name, password=password)
            db.session.add(new_user)
            db.session.commit()

            session['name'] = name
            session['logged_in'] = True
            # Return on signup (could change to an html file)
            users = User.query.all()
            return render_template("users.html", username = name, users = users)
        else:
            error = "Username already exists please try again."
            return render_template("signup.html", error = error)
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
    if __name__ == '__main__':
            db.create_all() 
            app.run(debug=True)