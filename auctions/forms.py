from django import forms
from .models import Listing, bid, Comment


# Create your forms here.
class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        #fields = ('categories', 'image', 'image_url', 'title', 'description', 'bid')
        fields = ('title', 'description', 'bid', 'categories', 'image_url')