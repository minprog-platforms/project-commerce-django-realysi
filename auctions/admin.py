from django.contrib import admin
from.models import User, Category, Listing, Comment, Bid

# Register your models here -> so you can see it in admin
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)