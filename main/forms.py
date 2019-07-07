import re

from marshmallow import Schema, fields, validate, EXCLUDE, validates
from marshmallow import validates_schema, ValidationError
from marshmallow.validate import Validator
from models import User

class Regexr(Validator):
    """Validate ``value`` against the provided regex.
    :param regex: The regular expression string to use. Can also be a compiled
        regular expression pattern.
    :param flags: The regexp flags to use, for example re.IGNORECASE. Ignored
        if ``regex`` is not a string.
    :param str error: Error message to raise in case of a validation error.
        Can be interpolated with `{input}` and `{regex}`.
    """

    default_message = "String does not match expected pattern."

    def __init__(self, regex, flags=0, min=0, max=1000, *, error=None):
        self.regex = (
            re.compile(regex, flags) if isinstance(regex, (str, bytes)) else regex
        )
        self.error = error or self.default_message

    def _repr_args(self):
        return "regex={!r}".format(self.regex)

    def _format_error(self, value):
        return self.error.format(input=value, regex=self.regex.pattern)

    def __call__(self, value):
        if self.regex.search(value) is not None:
            raise ValidationError(self._format_error(value))

        return value

class UserSchema(Schema):
    username= fields.String(
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


class UpdateUserSchema(Schema):
    user = fields.Nested(UserSchema)
    new_password = fields.Str(
        validate=[
            validate.Length(min=6, max=40, error='New password must be between 6 and 40 characters in length.'),
            validate.Regexp(r'\w.*', error='New password must only be contain letters and numbers.')
        ])

class ClientSchema(Schema):
    email = fields.Email(error='Email address is not valid.', required=True)
    name = fields.Str(
        validate=[
            validate.Length(min=2, max=40, error='Name must be between 2 and 40 characters in length.'),
            validate.Regexp(r'\w.*', error='Name must only include word characters.')
        ]
    )
    description = fields.Str(
        validate=[
            validate.Length(min=2, max=3000, error='Description must be between 2 and 300 characters in length.'),
            validate.Regexp(r'\w.*', error='Name must only include word characters.')
        ]
    )
