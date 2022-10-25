from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User
from django.db import models
from PIL import Image #for image field
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import datetime

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
    title = models.CharField(max_length=100)
    description = models.TextField()
    bid = models.IntegerField()

    HOME = 'HM'
    CLOTHES = 'CL'
    FURNITURE = 'FR'
    NONE = 'NA'
    CATEGORY = [
        (NONE, 'None'),
        (HOME, 'Home'),
        (CLOTHES, 'Clothes'),
        (FURNITURE, 'Furniture'),

    ]
    categories = models.CharField(
        max_length=2,
        choices=CATEGORY,
        default=NONE
    )


    image = models.ImageField(upload_to='media/Listings/ ', blank=True,max_length=100,required=False)
    image_url = models.URLField(required=False)


    user_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")
    creation_date = models.DateField(default=datetime.datetime.now()) #save on creation
    closed = models.BooleanField(default=False)
    finalized = models.BooleanField(default=False)
    final_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder_won", null=True)



    def __str__(self):
        return f'{self.title}'

    def update_bid(self,new_bid):
        self.bid = new_bid

    def close_listing(self):
        self.closed = True
    def open_listing(self):
        self.closed = False

    def finalize_listing(self, winner):
        self.finalized = True
        self.closed = True
        self.final_bidder = winner
    def save(self, *args, **kwargs):
        super(Listing, self).save(*args, **kwargs)
        if self.image_url and not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image.save(f"image_{self.pk}", File(img_temp))
            super(Listing, self).save(*args, **kwargs)




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
    creation_date = models.DateField(default=datetime.datetime.now())  # save on creation
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
    creation_date = models.DateField(default=datetime.datetime.now())  # save on creation
    #not used due to time constraint and lack of time management!
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE,
                                        related_name='child_comment', null=True, blank=True)

    def __str__(self):
        return  f'{self.comment}'