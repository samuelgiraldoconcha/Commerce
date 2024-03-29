from django.contrib.auth.models import AbstractUser
from django.db import models

    
class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = [('NC', 'No category'),
                  ('A', 'Aplications'),
                  ('RE', 'Real Estate'),
                  ('ED', 'Electronic devices'),]
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.CharField(max_length=24, choices=CATEGORIES, default='NC')
    title = models.CharField(max_length=24)
    description = models.CharField(max_length=64)
    price = models.FloatField()
    image_source = models.CharField(max_length=200)
    active = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.id}: {self.seller} sells this {self.title} {self.description} starting at {self.price}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    offering_price = models.FloatField()
    
    def __str__(self):
        return f"{self.id}: {self.bidder} is offering {self.offering_price}"
    
class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "comments")
    description = models.CharField(max_length=200, default=None)