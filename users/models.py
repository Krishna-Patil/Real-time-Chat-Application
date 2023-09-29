from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_online = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return super().__str__()

def login_tasks(sender, user, request, **kwargs):
    user.is_online = True
    user.save()
user_logged_in.connect(login_tasks)

def logout_tasks(sender, user, request, **kwargs):
    print(user.username)
    user.is_online = False
    user.save()
user_logged_out.connect(logout_tasks)
