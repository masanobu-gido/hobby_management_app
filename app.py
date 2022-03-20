from email import message
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from datetime import datetime
import pytz
import os
from werkzeug.security import generate_password_hash, check_password_hash
from score import hobby_score, hobby

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hobby.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20))
    


class LogArticle(db.Model):
    __tablename__ = 'hobbes'
    user_id = db.Column(db.Integer, nullable=False)
    log_id = db.Column(db.Integer, primary_key=True)
    hobby = db.Column(db.String(50), nullable=False)
    time = db.Column(db.Integer, nullable=True)
    feeling = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    



@app.route('/')
#@login_required
def top():
    if request.method == 'GET':
        logarticles = LogArticle.query.all()
        users = User.query.all()
        score, max_score = hobby_score(current_user.id)
        return render_template('top.html', logarticles=logarticles, user=current_user.username, score=score, max_score=max_score)
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('name')
        password = request.form.get('password')
        if User.query.filter_by(username=username).count() != 0 or len(username) == 0 or len(password) == 0:
            return render_template('resignup.html')
        else:
            user = User(username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
    else:
        return render_template('signup.html')


#@app.route('/resignup')
#def retry():
#    return redirect('/signup')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('name')
        password = request.form.get('password')
        if username == "" or password == "":
            return render_template('relogin.html')
        else:
            user = User.query.filter_by(username=username).first()
        
        if User.query.filter_by(username=username).count() == 0:
            return render_template('relogin.html')
        
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            return render_template('relogin.html')
        
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/log', methods=['GET', 'POST'])
@login_required
def log():
    if request.method == 'POST':
        hobby = request.form.get('hobby')
        time = int(request.form.get('time'))
        feeling = int(request.form.get('feeling'))
        user_id = current_user.id
        logarticle = LogArticle(user_id=user_id, hobby=hobby, time=time, feeling=feeling)
        db.session.add(logarticle)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('log.html')


"""@app.route('/new_hobby', methods=['GET', 'POST'])
@login_required
def new_hobby():
    if request.method == 'POST':
        hobby = request.form.get('hobby')
        logarticle = LogArticle(hobby=hobby, time=0)
        db.session.add(logarticle)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('new_hobby.html')
"""

@app.route('/account')
def account():
    hobbies = hobby(current_user.id)
    return render_template('account.html', user=current_user.username, hobbies=hobbies)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    logarticle = LogArticle.query.get(id)
    if request.method == 'GET':
        return render_template('edit.html', logarticle=logarticle)
    else:
        logarticle.hobby = request.form.get('hobby')
        logarticle.time = request.form.get('time')
        logarticle.feeling = request.form.get('feeling')
        db.session.commit()
        return redirect('/')


@app.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    logarticle = LogArticle.query.get(id)
    db.session.delete(logarticle)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    #db.create_all()
    app.run(port=12345, debug=True)