from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:trevorG2!@localhost/credentials'
app.secret_key = '\x14\xb1\x084\xcc\xc0\xb0\x1c>iW\xdf\x82u\x06B'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(user_id)

# create the thread form
class ThreadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create Thread')

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Comment')

class Thread(db.Model):
    __tablename__ = 'threads'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    author_name = db.Column(db.String, db.ForeignKey('user_info.username'))
    comments = db.relationship('Comment', backref='thread', lazy='dynamic')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    author_name = Column(String, ForeignKey('user_info.username'))
    thread_id = Column(Integer, ForeignKey('threads.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)

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
            login_user(user)
            session['logged_in'] = True  # Set session variable
            flash('Login successful')
            return redirect(url_for('index'))
        else:
            # Login failed
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('logged_in', None)  # Remove session variable
    flash('Logged out')
    return redirect(url_for('index'))

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

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    form = ThreadForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        thread = Thread(title=title, content=content, author_name=current_user.username)
        db.session.add(thread)
        db.session.commit()
        flash('Thread created')
        return redirect(url_for('forum'))
    else:
        threads = Thread.query.all()
        return render_template('forum.html', threads=threads, form=form)

@app.route('/create_thread', methods=['GET', 'POST'])
def create_thread():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        thread = Thread(title=title, content=content)
        db.session.add(thread)
        db.session.commit()
        return redirect(url_for('view_thread', thread_id=thread.id))
    else:
        return render_template('create_thread.html')

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            content = form.content.data
            comment = Comment(content=content, thread_id=thread_id, author_name=current_user.username)
            db.session.add(comment)
            db.session.commit()
            flash('Comment added')
            return redirect(url_for('view_thread', thread_id=thread_id))
    comments = Comment.query.filter_by(thread_id=thread_id).all()
    return render_template('view_thread.html', thread=thread, comments=comments, form=form)

if __name__ == '__main__':
    app.run()

    '''
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_login import LoginManager, login_required, current_user, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:trevorG2!@localhost/credentials'
app.secret_key = '\x14\xb1\x084\xcc\xc0\xb0\x1c>iW\xdf\x82u\x06B'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(user_id)

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)

class Thread(db.Model):
    __tablename__ = 'threads'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    author_name = db.Column(db.String, db.ForeignKey('user_info.username'))
    comments = db.relationship('Comment', backref='thread', lazy='dynamic')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    author_name = db.Column(db.String, db.ForeignKey('user_info.username'))
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'))

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
            login_user(user)
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

@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        thread = Thread(title=title, content=content, author_id=current_user.id)
        db.session.add(thread)
        db.session.commit()
        flash('Thread created')
        return redirect(url_for('forum'))
    else:
        threads = Thread.query.all()
        return render_template('forum.html', threads=threads)

@app.route('/create_thread', methods=['GET', 'POST'])
def create_thread():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        thread = Thread(title=title, content=content)
        db.session.add(thread)
        db.session.commit()
        return redirect(url_for('view_thread', thread_id=thread.id))
    else:
        return render_template('create_thread.html')

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    if request.method == 'POST':
        content = request.form['content']
        comment = Comment(content=content, thread_id=thread_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('view_thread', thread_id=thread_id))
    else:
        comments = Comment.query.filter_by(thread_id=thread_id).all()
        return render_template('view_thread.html', thread=thread, comments=comments)

if __name__ == '__main__':
    app.run()
'''