from django.db import models
from django.contrib.auth.models import User

class Purchased(models.Model):
    STATUS_CHOICES = [
        ('В ожидании', 'В ожидании'),
        ('В пути', 'В пути'),
        ('Прибыл', 'Прибыл'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=33)
    description = models.CharField(max_length=250)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/images/')
    email = models.EmailField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='В ожидании')

    def __str__(self):
        return self.author.username
