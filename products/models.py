from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock_count = models.IntegerField(default=0)

    class Meta:
        constraints=[
            models.CheckConstraint(condition=models.Q(price__gt=0),name='price__gt_0'),
            models.CheckConstraint(condition=models.Q(stock_count__gt=0),name='stock__gt_0')
        ]

    def get_discounted_price(self, discount_percentage):
        return self.price * (1 - discount_percentage/100)

    @property
    def in_stock(self) -> bool:
        return self.stock_count > 0





""" 
    def clean(self):
        if self.price < 0:
            raise ValidationError('Price cannot be negative')
        
        if self.stock_count < 0:
            raise ValidationError('stock_count cannot be negative')
         """
