from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name_category = models.CharField(max_length = 69)

    def __str__(self):
        return self.name_category


class Listing(models.Model):
    title = models.CharField(max_length = 69)
    description = models.CharField(max_length = 420)
    nation = models.CharField(max_length=100)
    url_image = models.CharField(max_length=4200)
    price = models.FloatField()
    active = models.BooleanField(default=True)
    beheerder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self) -> str:
        return self.title

# moet nog een bod model maken en ook comment dnek ik
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    message = models.CharField(max_length=420)

    def __str__(self) -> str:
        return f"{self.commenter} on {self.listing}"