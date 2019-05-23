from marshmallow import Schema, fields, validate
from marshmallow import validates_schema, ValidationError
from models import User

class UserSchema(Schema):
    email = fields.Email(error='Email address is not valid.', required=True)
    first_name = fields.Str(
        validate=[
            validate.Length(min=2, max=40, error='First Name must be between 2 and 40 characters in length.'),
            validate.Regexp(r'[A-Za-z]', error='First name must be only letters.')
        ])
    last_name = fields.Str(
        validate=[
            validate.Length(min=2, max=40, error='Last Name must be between 2 and 40 characfrom mters in length.'),
            validate.Regexp(r'[A-Za-z]', error='Last name must be only letters.')
        ])
    password = fields.Str(
        validate=[
            validate.Length(min=6, max=40, error='Password must be between 6 and 40 characters in length.'),
            validate.Regexp(r'\w', error='Password must only be contain letters and numbers.')
        ], load_only=True)

class UpdateUserSchema(Schema):
    user = fields.Nested(UserSchema)
    new_password = fields.Str(
        validate=[
            validate.Length(min=6, max=40, error='New password must be between 6 and 40 characters in length.'),
            validate.Regexp(r'\w', error='New password must only be contain letters and numbers.')
        ])