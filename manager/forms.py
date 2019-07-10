from marshmallow import Schema, fields, validate
from custom_forms import Regexr

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
