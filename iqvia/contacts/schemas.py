from flask_io import fields, Schema, post_load, validate
from .models import Contact, Email
from .services import validate_username


class EmailSchema(Schema):
    """
    serialization-deserialization-validation class for Emails.
    """
    email = fields.Email(required=True, validate=validate.Length(5, 128))

    @post_load
    def _post_load(self, data):
        if self.partial:
            return data
        return Email(**data)


class ContactSchema(Schema):
    """
    serialization-deserialization-validation class class for Contacts.
    """
    id = fields.UUID(dump_only=True)
    first_name = fields.String(50, required=True)
    surname = fields.String(50, required=True)
    username = fields.String(required=True, validator=validate_username,
                             error_messages={'validator_failed':
                                             {'message': 'Username must be 6-52 characters length and'
                                                         ' can only contain: a-zA-Z0-9.'}})
    inserted = fields.DateTime(dump_only=True)
    emails = fields.Nested(EmailSchema, exlude=('contact_id',), many=True)

    @post_load
    def _post_load(self, data):
        if self.partial:
            return data
        return Contact(**data)

