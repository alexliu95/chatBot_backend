from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from chatbot import db
from sqlalchemy import UniqueConstraint

#from langchain.chains.conversation.memory import CoversationBufferMemory
from langchain import OpenAI
from langchain.chains import ConversationChain
import os

class ChatMessage(db.Model):
    __tablename__ = 'chat_message'
    id= db.Column(db.Integer, primary_key=True)
    dialog_id = db.Column(db.String(20)) 
    sender_name = db.Column(db.String(20))
    receiver_name = db.Column(db.String(20))
    message = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, **kwargs):
        # Check if dialog_id exists
        dialog_id = kwargs.get('dialog_id')
        dialog = ChatDialog.query.get(dialog_id)
        if not dialog:
            return {'error': 'Dialog does not exist.'}, 400

        # If create_time is not provided, it will be set to current time by default
        new_chatmessage = cls(**kwargs)
        db.session.add(new_chatmessage)
        try:
            db.session.commit()
            return new_chatmessage, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    
    @classmethod
    def aichat(cls, **kwargs):
        openai_key = os.getenv('OPENAI_KEY', 'dev')
        return {
            'message':''
        }

    @classmethod
    def get_recent_messages(cls, dialog_id, round=1):
        return cls.query.filter_by(dialog_id=dialog_id).order_by(cls.create_time.desc()).limit(round).all()

class ChatDialog(db.Model):
    __tablename__ = 'chat_dialog'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30)) # usually chat group's name, chattee display name
    client_id = db.Column(db.String(20))
    user_id = db.Column(db.String(30), nullable=True) # chattee's open_id(wechat), or real user_id

    """client_id & name combined should be unique"""
    __table_args__ = (
        UniqueConstraint('name', 'client_id', 'user_id', name='unique_name_client_user'),
    )

    @classmethod
    def create(cls, **kwargs):
        dialog = cls.query.filter_by(**kwargs).first()
        if dialog:
            return {'error': 'Dialog with this client_id and name already exists.'}, 400

        new_dialog = cls(**kwargs)
        db.session.add(new_dialog)
        try:
            db.session.commit()
            return new_dialog, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    
    @classmethod
    def search(cls, client_id, name=None, user_id=None):
        if name:
            return cls.query.filter_by(client_id=client_id, name=name).first()
        elif user_id:
            return cls.query.filter_by(client_id=client_id, user_id=user_id).first()
        else:
            return None
        
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)