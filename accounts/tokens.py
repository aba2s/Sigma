"""
Generate Token: We need to create the token that will be used
in email confirmation URL.
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator  
import six
from django.contrib import messages

class TokenGenerator(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):  
        return (  
            six.text_type(user.pk) + six.text_type(timestamp) +  
            six.text_type(user.is_active)  
        )  
account_activation_token = TokenGenerator()
