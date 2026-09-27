from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.conf import settings

User=get_user_model()

class UserSignalsTest(TestCase):

    @patch('products.signals.send_mail')
    def test_welcome_email_sent_on_user_creation( self ,mock_send_mail):

        User.objects.create_user(username='john',email='john@example.com',password='password123')

        mock_send_mail.assert_called_once_with(
            subject="Wellcom!",
            message="thanks for signing up !",
            from_email=settings.DEFAULT_FROM_EMAIL ,
            recipient_list=['john@example.com'],
            fail_silently=False
                    
        )

    @patch('products.signals.send_mail')
    def test_no_email_sent_on_user_update(self, mock_send_mail):
        user=User.objects.create_user(username='john',email='john@example.com',password='password123')

        mock_send_mail.reset_mock()

        user.email='john_new@example.com'
        user.save()

        mock_send_mail.assert_not_called()
 