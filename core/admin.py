""" from django.contrib import admin
from .models import User,Order
from django.conf import settings """

# Register your models here.


""" 
instead of defining a method separately from the 
the admin class we can still define the method within 
the admin class by doing so instead


@admin.action(description="Mark selected orders as shipped")
def order_shipped_action(self,request,queryset):
   do something ....
   

self.message_user(
            request,
            'Selected orders have been marked as shipped and users have been notified'
        )

then within the admin class   you pass the method as string 

actions=['method name']

 """

""" 

@admin.action(description="Mark selected orders as shipped")
def order_shipped_action(modeladmin,request,queryset):
    orders_to_ship=queryset.exclude(status=Order.OrderStatus.SHIPPED)
    orders = list(orders_to_ship)
    orders_to_ship.update(status=Order.OrderStatus.SHIPPED)

    # email user

    for order in orders:
        user = order.user
        user.email_user(
            subject="Your order has been shipped",
            message=f"Dear {user.username},\n\nYour order with ID {user.id} has been shipped",
            from_email=settings.DEFAULT_FROM_EMAIL ,
            fail_silently=False
        )

        modeladmin.message_user(
            request,
            'Selected orders have been marked as shipped and users have been notified'
        ) """
""" 
@admin.action(description="Mark selected orders as delivered")
def order_delivered_action(modeladmin,request,queryset):
    orders_to_delivered=queryset.exclude(status=Order.OrderStatus.DELIVERED)
    orders = list(orders_to_delivered)
    orders_to_delivered.update(status=Order.OrderStatus.DELIVERED)

    # email user

    for order in orders:
        user = order.user
        user.email_user(
            subject="Your order has been shipped",
            message=f"Dear {user.username},\n\nYour order with ID {user.id} has been shipped",
            from_email=settings.DEFAULT_FROM_EMAIL ,
            fail_silently=False
        )

        modeladmin.message_user(
            request,
            'Selected orders have been marked as delivered and users have been notified'
        )

@admin.action(description="Mark selected orders as delivered")
def order_pending_action(modeladmin,request,queryset):
    orders_to_pending=queryset.exclude(status=Order.OrderStatus.PENDING)
    orders = list(orders_to_pending)
    orders_to_pending.update(status=Order.OrderStatus.PENDING)

    # email user

    for order in orders:
        user = order.user
        user.email_user(
            subject="Your order has been shipped",
            message=f"Dear {user.username},Your order with ID {user.id} has been shipped",
            from_email=settings.DEFAULT_FROM_EMAIL ,
            fail_silently=False
        )

        modeladmin.message_user(
            request,
            'Selected orders have been marked as pending and users have been notified'
        )



 """

""" 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
pass 
   """  
"""
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','status','created_at','updated_at']
    list_editable=['status']
    actions = [order_shipped_action,order_delivered_action,order_pending_action]
    
 """