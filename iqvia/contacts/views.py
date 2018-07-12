from flask import Blueprint
from flask_io import fields
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from .services import does_contact_username_exist
from .schemas import ContactSchema
from .models import Contact, Email
from .. import db, io

app = Blueprint('contacts', __name__, url_prefix='/contacts')


@app.route('/', methods=['POST'])
@io.from_body('contact', ContactSchema)
@io.marshal_with(ContactSchema)
def add_contact(contact):
    """
    @api {post} /contacts Adds a contact
    @apiDescription Adds a new contact
    @apiName add_contact
    @apiGroup Contacts

    @apiParam (Body) {String{1-50}}      first_name           The first name of the contact.
    @apiParam (Body) {String{1-50}}      surname              The surname of the contact.
    @apiParam (Body) {String{6-32}}      username             The username of the contact.
    @apiParam (Body) {Array}             emails               The emails of the contact.
    @apiParam (Body) {String{5-128}}     emails.email         The email address.

    @apiSuccess {UUID}                   id                   The ID of the contact.
    @apiSuccess {String{1-50}}           first_name           The first name of the contact.
    @apiSuccess {String{1-50}}           surname              The surname of the contact.
    @apiSuccess {String{6-32}}           username             The username of the contact.
    @apiSuccess {Datetime}               inserted             The insertion time of the contact.
    @apiSuccess {Array}                  emails               The emails of the contact.
    @apiSuccess {String{5-128}}          emails.email         The email address.
    """
    contact.id = str(uuid4())
    if does_contact_username_exist(contact.username):
        return io.bad_request('Sorry, the username {} of the contact you try '
                              'to add already exists'.format(contact.username))

    db.session.merge(contact)
    db.session.commit()
    return contact


@app.route('/', methods=['GET'])
@io.marshal_with(ContactSchema, envelope='contacts')
def get_contacts():
    """
    @api {get} /contacts Gets all the contacts
    @apiDescription Gets all the contacts
    @apiName get_contacts
    @apiGroup Contacts

    @apiSuccess {Array}                  contacts                The contacts retrieved.
    @apiSuccess {UUID}                   contacts.id             The ID of the contact.
    @apiSuccess {String{1-50}}           contacts.first_name     The first name of the contact.
    @apiSuccess {String{1-50}}           contacts.surname        The surname of the contact.
    @apiSuccess {String{6-32}}           contacts.username       The username of the contact.
    @apiSuccess {Datetime}               contacts.inserted       The insertion time of the contact.
    @apiSuccess {Array}                  contacts.emails         The emails of the contact.
    @apiSuccess {String{5-128}}          contacts.emails.email   The email address.
    """
    return Contact.query.options(joinedload(Contact.emails)).all()


@app.route('/contact', methods=['GET'])
@io.marshal_with(ContactSchema)
@io.from_query('username', fields.String())
@io.from_query('email', fields.Email())
def get_contact(username, email):
    """
    @api {get} /contacts/<username> Gets a contact
    @apiDescription Gets a contact with filters
    @apiName get_contact
    @apiGroup Contacts

    @apiParam {String{6-32}}             [username]           The Username of the contact.
    @apiParam {String{5-128}}            [email]              The email address of the contact.

    @apiSuccess {UUID}                   id                   The ID of the contact.
    @apiSuccess {String{1-50}}           first_name           The first name of the contact.
    @apiSuccess {String{1-50}}           surname              The surname of the contact.
    @apiSuccess {String{6-32}}           username             The username of the contact.
    @apiSuccess {Datetime}               inserted             The insertion time of the contact.
    @apiSuccess {Array}                  emails               The emails of the contact.
    @apiSuccess {String{5-128}}          emails.email         The email address.
    """
    contact_query = Contact.query.options(joinedload(Contact.emails))

    if not username and not email:
        return io.bad_request('Sorry, you need to provide at least one filter in the query (username or email)')

    if username:
        contact_query = contact_query.filter(Contact.username == str(username))
    if email:
        contact_query = contact_query.filter(Contact.emails.any(Email.email == email))

    return contact_query.first()


@app.route('/<uuid:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """
    @api {delete} /contacts/<contact_id> Deletes a contact
    @apiDescription Deletes a contact
    @apiName delete_contact
    @apiGroup Contacts

    @apiParam {UUID}  contact_id  The ID of the contact.
    """
    contact = Contact.query.filter(Contact.id == str(contact_id)).first()
    if not contact:
        return io.bad_request('Sorry, the contact {} you try to delete does not exist'.format(contact_id))

    db.session.delete(contact)
    db.session.commit()


@app.route('/<int:inserted_seconds>', methods=['DELETE'])
def delete_contacts(inserted_seconds):
    """
    @api {delete} /contacts/<contact_id> Deletes contacts
    @apiDescription Deletes contacts
    @apiName delete_contacts
    @apiGroup Contacts

    @apiParam {Integer}  inserted_seconds  Deletes all the contacts inserted before inserted_seconds ago.
    """
    datetime_remove_from = datetime.now() - timedelta(seconds=inserted_seconds)

    # Avoid loading the contacts in memory before deleting as it can be a lot of them.
    delete_command = Contact.__table__.delete().where(Contact.inserted < datetime_remove_from)

    db.engine.execute(delete_command)


@app.route('/<uuid:contact_id>', methods=['PATCH', 'PUT', 'POST'])
@io.from_body('contact_data', ContactSchema(partial=True))
@io.marshal_with(ContactSchema())
def update_contact(contact_id, contact_data):
    """
    @api {patch} /contacts/<contact_id> Updates an item
    @apiDescription Updates a contact
    @apiName update_contact
    @apiGroup Contacts

    @apiParam (Body) {String{1-50}}      [first_name]         The first name of the contact.
    @apiParam (Body) {String{1-50}}      [surname]            The last name of the contact.
    @apiParam (Body) {String{1-32}}      [username]           The username of the contact.
    @apiParam (Body) {Array}             [emails]             The emails of the contact.
    @apiParam (Body) {String{5-128}}     [emails.email]       The email address.

    @apiSuccess {UUID}                   id                   The ID of the contact.
    @apiSuccess {String{1-50}}           first_name           The first name of the contact.
    @apiSuccess {String{1-50}}           surname              The surname of the contact.
    @apiSuccess {String{6-32}}           username             The username of the contact.
    @apiSuccess {Datetime}               inserted             The insertion time of the contact.
    @apiSuccess {Array}                  emails               The emails of the contact.
    @apiSuccess {String{5-128}}          emails.email         The email address.
    """
    contact = Contact.query.options(joinedload(Contact.emails)).filter(Contact.id == str(contact_id)).first()
    if not contact:
        return io.bad_request('Sorry, the contact {} you try to update does not exist'.format(contact_id))

    if 'username' in contact_data and contact.username != contact_data['username'] and \
            does_contact_username_exist(contact_data['username']):
        return io.bad_request('Sorry, you cannot update the contact '
                              'with the username {}: it already exists'.format(contact_data['username']))

    if 'first_name' in contact_data:
        contact.first_name = contact_data['first_name']
    if 'surname' in contact_data:
        contact.surname = contact_data['surname']
    if 'username' in contact_data:
        contact.username = contact_data['username']
    if 'emails' in contact_data:
        contact.emails = contact_data['emails']

    db.session.merge(contact)
    db.session.commit()
    return contact
