"""
Generate Token: We need to create the token that will be used
in email confirmation URL.
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)  # noqa: 503
            + six.text_type(user.is_active)  # noqa: 503
        )


account_activation_token = TokenGenerator()
