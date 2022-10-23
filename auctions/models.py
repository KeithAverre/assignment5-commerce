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
        -current bid --> starting bid at creation
        -Comments
"""

"""
MODEL: bid for listing

TODO:
    -add fields:
        -User who is bidding
        -bid amount
        -parent listing
        
    RELATIONSHIP: many to one with listing
        many bids per listing but only one listing per bid

"""

"""
MODEL: Comments for listing

TODO:
    -add fields:
        -User who is commenting
        -text of comment
        
    -possible fields:
        -possible parent listing
        -possible parent comment
        
    
    RELATIONSHIP: many to one with listing
        many comments per listing but only one listing per comment
        
                  many to zero or one with comment
        many comments per parent comment but only zero or one parent comment per comment

"""