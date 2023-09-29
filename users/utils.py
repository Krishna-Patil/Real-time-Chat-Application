from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import CustomUser


def is_online(username_or_id):
    """
    checks whether the user is available/online or not
    """
    try:
        if type(username_or_id) == str:
            user = CustomUser.objects.get(username=username_or_id)
        else:
            user = CustomUser.objects.get(id=username_or_id)
        if user.is_online:
            return True
        return False
    except Exception as e:
        return e 


def get_user(token):
    """
    returns user using jwt token
    """
    try:
        access_token = AccessToken(token)
        user = CustomUser.objects.get(id=access_token['user_id'])
        return user
    except TokenError:
        return TokenError

