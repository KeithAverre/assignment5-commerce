from django.contrib import admin
from .models import Listing, bid, Comment,User

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(bid)
admin.site.register(Comment)
# Register your models here.
