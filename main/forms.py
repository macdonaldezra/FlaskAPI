from marshmallow import Schema, fields, validate
from marshmallow import validates_schema, ValidationError


class UserRegistrationSchema(Schema):
    email = fields.Email(
        required=True,
        validate=validate.Email(error='Not a valid email address')
    )
    first_name = fields.Str(validate=validate.Length(min=2, max=40,
                            error='First Name must be between 2 and 40 characters in length'))
    last_name = fields.Str(validate=validate.Length(min=2, max=40,
                           error='Last Name must be between 2 and 40 characfrom mters in length'))
    password = fields.Str(validate=validate.Length(min=6, max=40,
                          error='Password must be between 6 and 40 characters in length'))

    @validates_schema
    def validate_email(self, data):
        if len(data['email']) < 3:
            raise ValidationError('Email must be more than 3 characters.')
        elif 100 < len(data['email']):
            raise ValidationError('Email must not be longer than 100 characters.')