from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import uuid

SQLALCHEMY_DATABASE_URI = 'sqlite:///iqvia.db'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iqvia.db'

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)


class Contact(UserMixin, db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    first_name = db.Column(String(50), nullable=False)
    surname = db.Column(String(50), nullable=False)
    username = db.Column(String(32), nullable=False, unique=True)

    emails = relationship('Email', cascade='all, delete, delete-orphan', lazy='noload')


class Email(db.Model):
    __tablename__ = 'emails'

    email = db.Column(db.Text(length=128), primary_key=True)
    contact_id = db.Column(ForeignKey('contacts.id', ondelete='CASCADE'))

    contact = relationship('Contact', lazy='noload')


with app.app_context():
    db.create_all()
