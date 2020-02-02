import re

from marshmallow import ValidationError

from marshmallow.validate import Validator

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