from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User
from django.db import models
from PIL import Image #for image field

"""
MODEL: USER

TODO:
    -add fields:
        -Watchlist -> a list of listings
        

Known bugs:

"""
class User(AbstractUser):
    pass


"""
MODEL: listing

TODO:
    -add fields:
        -title -charfield **
        -image -img field **
        -Description -textfield **
        -user who made it -user foreign key **
        -categories -choice field **
        -current bid --> starting bid at creation  -integer field**
        -Comments 
        -Time of post datetime field**
"""
class Listing(models.Model):
    HOME = 'HM'
    CLOTHES = 'CL'
    FURNITURE = 'FR'
    NONE = 'NA'
    CATEGORY = [
        (HOME, 'Home'),
        (CLOTHES, 'Clothes'),
        (FURNITURE, 'Furniture'),
        (NONE, 'None'),
    ]
    categories = models.CharField(
        max_length=2,
        choices=CATEGORY,
        default=NONE
    )

    # width and height might be a problem and file size
    image = models.ImageField(upload_to='images/', blank=True,max_length=100)
    image_url = models.URLField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")
    bid = models.IntegerField() #integer for money value?
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True) #save on creation


    def __str__(self):
        return f'{self.title}'




"""
MODEL: bid for listing

TODO:
    -add fields:
        -User who is bidding -> user foreign key
        -bid amount -integer field
        -parent listing -> listing foreign key
        
    RELATIONSHIP: many to one with listing
        many bids per listing but only one listing per bid

"""
class bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_owner")
    amount = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="parent_listing")

    def __int__(self):
        return self.amount



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
class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_owner")
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_parent_listing")
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE,
                                        related_name='child_comment', null=True, blank=True)

    def __str__(self):
        return  f'{self.comment}'