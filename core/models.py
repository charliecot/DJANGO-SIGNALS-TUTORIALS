from django.db import models
from django.contrib.auth.models import  AbstractUser

# Create your models here.
""" 
class User(AbstractUser):
    cv = models.FileField(upload_to='cvs',null=True,blank=True)



class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING ='pending'
        SHIPPED = 'shipped'
        DELIVERED = 'delivered'
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    status= models.CharField(max_length=20,choices=OrderStatus,default='Pending')   
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return  f'Order {self.id} by {self.user.username}' """