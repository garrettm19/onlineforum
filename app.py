from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:trevorG2!@localhost/credentials'
app.secret_key = '\x14\xb1\x084\xcc\xc0\xb0\x1c>iW\xdf\x82u\x06B'
db = SQLAlchemy(app)

try:
    result = db.engine.execute('SELECT 1')
    print('Database connection successful:', result.fetchone())
except Exception as e:
    print('Database connection failed:', e)

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Query the user_info table to check if the provided username and password are valid
        user = UserInfo.query.filter_by(username=username, password=password).first()
        if user:
            # Login successful
            flash('Login successful')
            return redirect(url_for('index'))
        else:
            # Login failed
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Check if the provided username already exists in the user_info table
        user = UserInfo.query.filter_by(username=username).first()
        if user:
            # Username already exists
            flash('Username already taken', 'error')
            return redirect(url_for('register'))
        elif password == confirm_password:
            # Create a new user and add it to the user_info table
            new_user = UserInfo(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            # Registration successful
            flash('Registration successful')
            return redirect(url_for('login'))
        else:
            # Registration failed
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
    else:
        return render_template('register.html')

@app.route('/forum')
def forum():
    # Add your forum logic here
    return 'Welcome to the forum!'

if __name__ == '__main__':
    app.run()