from django import forms
from .models import Category, Listing, bid, Comment


# Create your forms here.
class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        #fields = ('categories', 'image', 'image_url', 'title', 'description', 'bid')
        fields = ('title', 'description', 'bid', 'categories', 'image', 'image_url')


class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())