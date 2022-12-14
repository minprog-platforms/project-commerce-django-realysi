from django.contrib import admin
from.models import User, Category, Listing

# Register your models here -> so you can see it in admin
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)