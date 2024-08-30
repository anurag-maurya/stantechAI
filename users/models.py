from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    '''
    Using Django's built in User model.
    '''
    pass

