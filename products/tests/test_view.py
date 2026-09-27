from django.test import TestCase,SimpleTestCase
from products.models import Product
from django.contrib.auth import get_user_model
from django.urls import reverse
import requests
from unittest.mock import patch

User = get_user_model()



class PostsViewTest(TestCase):
    
    @patch('products.views.requests.get')
    def test_post_view_success(self,mock_get):

        mock_get.return_value.status_code = 200

        return_data={
            'userId':1,
            'id': 1,
            'title':'Test Title',
            'body': 'Test Body'
        }

        mock_get.return_value.json.return_value = return_data


        response = self.client.get(reverse('post'))

        self.assertJSONEqual(response.content,return_data)
        mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/posts/1')

    @patch('products.views.requests.get')
    def test_post_view_fails(self,mock_get):
        mock_get.side_effect = requests.exceptions.RequestException

        response = self.client.get(reverse('post'))

        self.assertEqual(response.status_code,503)

        mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/posts/1')




class TestProfilePage(TestCase):

    def test_profile_view_redirect_for_anonymous_users(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response,expected_url=f"{reverse('login')}?next={reverse('profile')}")


    def test_profile_view_accessible_for_authenticated_users(self):
        User.objects.create_user(username='testuser',password='password123')

        self.client.login(username='testuser',password='password123')
        response= self.client.get(reverse('profile'))

        self.assertContains(response,'testuser')







class TestHomePage(SimpleTestCase):

    def test_hompage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)

    def test_homepage_uses_correct_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response,'index.html')

    def test_homepage_contains_welcome_message(self):
        response = self.client.get('/')
        self.assertContains(response,'Hello Django',status_code=200)



class TestProductPage(TestCase):

    def setUp(self):
        
        Product.objects.create(name='Laptop', price=1000,stock_count=5)
        Product.objects.create(name='Phone', price=800 , stock_count=10)


    def test_products_uses_correct_template(self):
        response = self.client.get(reverse('products'))
        self.assertTemplateUsed(response,'products.html')


    def test_products_context(self):
        response = self.client.get(reverse('products')) 
        self.assertEqual(len(response.context['products']),2) 
        self.assertContains(response,'Laptop')
        self.assertContains(response,'Phone')
        self.assertNotContains(response,'no products available')


    def test_products_view_no_products(self):
        Product.objects.all().delete()  
        response = self.client.get(reverse('products'))  
        self.assertContains(response,'no products available') 
        self.assertEqual(len(response.context['products']),0) 










