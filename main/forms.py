import re

from marshmallow import Schema, fields, validate, EXCLUDE
from marshmallow import ValidationError
from marshmallow.validate import Validator
from custom_forms import Regexr

class UserSchema(Schema):
    username = fields.String(
        validate=[
            validate.Length(min=6, max=40, error='Username must be between 6 and 40 characters in length.'),
            Regexr(r'\W', error='Username must contain only letters, numbers, and underscores.')
        ],
        required=True
    )
    email = fields.Email(error='Email address is not valid.')
    first_name = fields.Str(
        validate=[
            validate.Length(min=2, max=40, error='First Name must be between 2 and 40 characters in length.'),
            Regexr(r'[^A-Za-z]', error='First name must contain only letters.')
        ]
    )
    last_name = fields.Str(
        validate=[
            validate.Length(min=2, max=40, error='Last Name must be between 2 and 40 characfrom mters in length.'),
            Regexr(r'[^A-Za-z]', error='Last name must contain only letters.')
        ]
    )
    password = fields.Str(
        validate=[
            validate.Length(min=6, max=40, error='Password must be between 6 and 40 characters in length.'),
            Regexr(r'\W', error='Password must contain only letters, numbers, and underscores.')
        ],
        load_only=True
    )
    clients = fields.Nested("ClientSchema", exclude=['projects'], many=True, dump_only=True, allow_none=True)

class UpdateUserSchema(Schema):
    user = fields.Nested(UserSchema)
    new_password = fields.Str(
        validate=[
            validate.Length(min=6, max=40, error='New password must be between 6 and 40 characters in length.'),
            Regexr(r'\W', error='New password must only be contain letters and numbers.')
        ])

class ConfirmUserPasswordSchema(Schema):
    confirm_password = fields.Str(
        validate=[
            validate.Length(min=6, max=40, error='New password must be between 6 and 40 characters in length.'),
            Regexr(r'\W', error='New password must only be contain letters and numbers.')
        ])
class ClientSchema(Schema):
    email = fields.Email(error='Email address is not valid.', required=True)
    name = fields.Str(
        validate=[
            validate.Length(min=2, max=40, error='Name must be between 2 and 40 characters in length.'),
            Regexr(r'\W', error='Name must contain only letters, numbers, and underscores.')
        ], required=True
    )
    description = fields.Str(
        validate=[
            validate.Length(min=5, max=500, error='Description must be between 2 and 300 characters in length.'),
            Regexr(r'[^\w\-.,;\ !?&\/:]', error='Description must contain only letters, numbers, underscores, and punctuation.')
        ]
    )
    projects = fields.Nested("ProjectSchema", many=True, dump_only=True, allow_none=True)

class ProjectSchema(Schema):
    name = fields.Str(
        validate=[
            validate.Length(min=2, max=40, error='Name must be between 2 and 40 characters in length.'),
            Regexr(r'\W', error='Name must contain only letters, numbers, and underscores.')
        ], required=True
    )
    description = fields.Str(
        validate=[
            validate.Length(min=5, max=500, error='Description must be between 2 and 300 characters in length.'),
            Regexr(r'[^\w\-.,;\ !?&\/:]', error='Description must contain only letters, numbers, underscores, and punctuation.')
        ]
    )