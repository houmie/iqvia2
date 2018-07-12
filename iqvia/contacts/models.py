from sqlalchemy import String, ForeignKey, Column, text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from .. import db


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = Column(UUID, primary_key=True)
    first_name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    username = Column(String(32), nullable=False, unique=True)
    inserted = Column(DateTime(True), nullable=False, default=lambda: datetime.now(), server_default=text("now()"))

    emails = relationship('Email', cascade='all, delete, delete-orphan', lazy='noload')


class Email(db.Model):
    __tablename__ = 'emails'

    email = db.Column(db.Text(length=128), primary_key=True)
    contact_id = db.Column(ForeignKey('contacts.id', ondelete='CASCADE'))

    contact = relationship('Contact', lazy='noload')
