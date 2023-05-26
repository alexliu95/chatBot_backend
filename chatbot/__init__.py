import os
import sys

from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = APIFlask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'

@login_manager.user_loader
def load_user(user_id):
    from chatbot.models import User
    user = User.query.get(int(user_id))
    return user

@app.context_processor
def inject_user():
    from chatbot.models import User
    user = User.query.first()
    return dict(user=user)

from chatbot import views, errors, commands, apis
