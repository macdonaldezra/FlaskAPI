from marshmallow import Schema, fields, validate
from marshmallow.validate import Validator
from utils.custom_forms import Regexr


class UserSchema(Schema):
    """Validate provided user information."""
    username = fields.String(
        validate=[
            validate.Length(min=6, max=40, 
                error='Username must be between 6 and 40 characters in length.'),
            Regexr(r'\W', error='Username must contain only letters, numbers, and underscores.')
        ],
        required=True
    )
    email = fields.Email(error='Email address is not valid.')
    first_name = fields.Str(
        validate=[
            validate.Length(min=2, max=40, 
                error='First Name must be between 2 and 40 characters in length.'),
            Regexr(r'[^A-Za-z]', error='First name must contain only letters.')
        ]
    )
    last_name = fields.Str(
        validate=[
            validate.Length(min=2, max=40, 
                error='Last Name must be between 2 and 40 characfrom mters in length.'),
            Regexr(r'[^A-Za-z]', error='Last name must contain only letters.')
        ]
    )
    password = fields.Str(
        validate=[
            validate.Length(min=6, max=40, 
                error='Password must be between 6 and 40 characters in length.'),
            Regexr(r'\W', error='Password must contain only letters, numbers, and underscores.')
        ],
        load_only=True
    )
    clients = fields.Nested("ClientSchema", exclude=['projects'],
        many=True, dump_only=True, allow_none=True)

class UpdateUserSchema(Schema):
    """Validate a user's new password along with their other information."""
    user = fields.Nested(UserSchema)
    new_password = fields.Str(
        validate=[
            validate.Length(min=6, max=40, 
                error='New password must be between 6 and 40 characters in length.'),
            Regexr(r'\W', error='New password must only be contain letters and numbers.')
        ])

class ConfirmUserPasswordSchema(Schema):
    """Validate length and characters for password."""
    confirm_password = fields.Str(
        validate=[
            validate.Length(min=6, max=40, 
                error='New password must be between 6 and 40 characters in length.'),
            Regexr(r'\W', error='New password must only be contain letters and numbers.')
        ])

