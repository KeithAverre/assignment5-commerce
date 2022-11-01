from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User
from django.db import models
from PIL import Image #for image field
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile

from django.utils import timezone

"""
MODEL: USER

TODO:
    -add fields:
        -Watchlist -> a list of listings
        

Known bugs:

"""
class User(AbstractUser):
    watchlist = models.CharField(max_length=1000, default="")#not a future proof solution

    def watch(self):
        if self.watchlist.count(",") == 0 or self.watchlist =="" or self.watchlist ==",":
            return []
        elif self.watchlist.count(",") == 1:
            f = self.watchlist.index(",")
            return [self.watchlist[0:f]]
        k = []
        for i in list(self.watchlist.split(",")):
            if i != "":
                k.append(int(i))
        return k
    def add_to_watchlist(self,s):
        if len(self.watchlist) == 0:
            self.watchlist += f'{s},'
        else:
            self.watchlist += f'{s},'

    def remove_from_watchlist(self,s):

        if(self.watchlist[0:s] == str(s)):
            self.watchlist=self.watchlist[s:]

        self.watchlist= self.watchlist.replace(f',{s},',",")


    def clear_watchlist(self):
        self.watchlist =""
    pass


"""
MODEL: listing

TODO:
    -add fields:ew
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

    # HOME = 'HM'
    # CLOTHES = 'CL'
    # FURNITURE = 'FR'
    # NONE = 'NA'
    # CATEGORY = [
    #     (NONE, 'None'),
    #     (HOME, 'Home'),
    #     (CLOTHES, 'Clothes'),
    #     (FURNITURE, 'Furniture'),

    # ]
    # categories = models.CharField(
    #     max_length=2,
    #     choices=CATEGORY,
    #     default=NONE
    # )


    image = models.ImageField(upload_to='images/',max_length=100,blank=True, null=True)
    image_url = models.URLField(blank=True)

    categories = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")
    #creation_date = models.DateField(default=datetime.datetime.now()) #save on creation
    closed = models.BooleanField(default=False)
    finalized = models.BooleanField(default=False)
    final_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder_won", null=True, blank=True)



    def __str__(self):
        return f'{self.title}'

    def update_bid(self,new_bid,new_bidder):
        self.bid = new_bid
        self.final_bidder = new_bidder

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
    #creation_date = models.DateField(default=datetime.datetime.now())  # save on creation
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
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    last_updated = models.DateTimeField(auto_now=True)

    #creation_date = models.DateField(default=datetime.datetime.now())  # save on creation
    #not used due to time constraint and lack of time management!
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE,
                                        related_name='child_comment', null=True, blank=True)

    def __str__(self):
        return  f'{self.comment}'


class Category(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/categories', blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name