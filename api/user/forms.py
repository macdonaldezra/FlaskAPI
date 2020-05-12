from marshmallow import Schema, fields, validate
from marshmallow.validate import Validator

from utils.custom_forms import Regexr


class ClientSchema(Schema):
    """Validate a new clients email, name and description."""
    email = fields.Email(error='Email address is not valid.', required=True)
    name = fields.Str(
        validate=[
            validate.Length(min=2, max=40, 
                error='Name must be between 2 and 40 characters in length.'),
            Regexr(r'\W', error='Name must contain only letters, numbers, and underscores.')
        ], required=True
    )
    description = fields.Str(
        validate=[
            validate.Length(min=5, max=500, 
                error='Description must be between 2 and 300 characters in length.'),
            Regexr(r'[^\w\-.,;\ !?&\/:]', 
                error='Description must contain only letters, numbers, underscores, and punctuation.')
        ]
    )
    projects = fields.Nested("ProjectSchema", many=True, dump_only=True, allow_none=True)


class ProjectSchema(Schema):
    """Validate a new project name and description."""
    name = fields.Str(
        validate=[
            validate.Length(min=2, max=40, 
                error='Name must be between 2 and 40 characters in length.'),
            Regexr(r'\W', error='Name must contain only letters, numbers, and underscores.')
        ], required=True
    )
    description = fields.Str(
        validate=[
            validate.Length(min=5, max=500, 
                error='Description must be between 2 and 300 characters in length.'),
            Regexr(r'[^\w\-.,;\ !?&\/:]', 
                error='Description must contain only letters, numbers, underscores, and punctuation.')
        ]
    )