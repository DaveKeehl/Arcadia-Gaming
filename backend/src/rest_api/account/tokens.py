from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()

# Line 1 – we import django password token generator. This class generate a token without persisting it to the database, yet it’s still able to determine whether the token is valid or not.

# Line 2 – we import six from django utils. Six provides simple utilities for wrapping over differences between Python 2 and Python 3.

# Line 4 – we create TokenGenerator class an pass an Instance of PasswordTokenGenerator.

# Line 5 – we create a method _make_hash_value which overrides PasswordTokenGenerator method.

# Line 6 – we return user id, timestamp and user is active using the six imported from django utils.

# Line 11 – we create variable and we equate it to our token generator class.