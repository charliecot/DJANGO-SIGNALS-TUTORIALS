from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
import os

User=get_user_model()



@receiver(post_delete, sender=User,dispatch_uid='clean_file_system')
def delete_associated_file(sender,instance,**kwargs):
    if instance.cv:
        if os.path.isfile(instance.cv.path):
            os.remove(instance.cv.path)




@receiver(post_save, sender=User,dispatch_uid="send_welcome_email")
def send_welcome_email(sender,instance,created,**kwargs):
    print('signal fired....')
    if created:
        send_mail(
            subject="Wellcom!",
            message="thanks for signing up !",
            from_email=settings.DEFAULT_FROM_EMAIL ,
            recipient_list=[instance.email],
            fail_silently=False
        )