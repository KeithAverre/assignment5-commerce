from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User
from django.db import models


class User(AbstractUser):
    pass


"""
MODEL: listing

TODO:
    -add fields:
        -title
        -image
        -Description
        -user who made it
        -categories
        -starting bid allowed

"""

"""
MODEL: bid for listing

TODO:

"""

"""
MODEL: Comments for listing

TODO:

"""