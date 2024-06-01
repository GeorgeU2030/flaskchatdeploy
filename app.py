from flask import Flask, render_template, request, session, redirect, url_for
from src.config import config
from models import User, db

from werkzeug.security import check_password_hash, generate_password_hash
from expert import Light, RobotCrossStreet
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/index', methods=['GET', 'POST'])
def index():
    response = None

    user_id = session.get('user_id')
    print('user_id', user_id)
    if user_id is None:
        return redirect(url_for('login'))
    

    user = User.query.filter_by(id=user_id).first()

    if request.method == 'POST':
        light_color = request.form.get('light_color')
        # Instantiate the system
        system = RobotCrossStreet()

        # Feed the facts to the system and run it
        system.reset()
        system.declare(Light(color=light_color))
        system.run()
        response = system.response
        print(response)
        

    return render_template('index.html', response=response, user=user)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.password, password):
            return render_template('auth/login.html', error='Invalid email or password')

        session['user_id'] = user.id
        return redirect(url_for('index'))
            
    else:
        return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('auth/register.html')

app.config.from_object(config['development'])
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()