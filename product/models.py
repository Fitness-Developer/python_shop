from django.db import models
from django.contrib.auth.models import User
class Product(models.Model):
    title = models.CharField(max_length=33)
    description = models.CharField(max_length=250)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/images/')
    def __str__(self):
        return self.title

class ReviewsOfProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    memo = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username







