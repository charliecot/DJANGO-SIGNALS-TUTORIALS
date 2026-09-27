from django.test import TestCase
from products.models import Product
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class ProductModelTest(TestCase):


    @classmethod
    def setUpTestData(cls):
       
       cls.product=Product(name='Test Product',price=100.00,stock_count=10)
       
       cls.negProduct= Product(name='Negative Price Product',price=-1.00,stock_count=5)

    def test_in_stock_property(self):

        self.assertTrue(self.product.in_stock)

        self.product.stock_count=0

        self.assertFalse(self.product.in_stock)

    def test_get_discount_price(self):

        self.assertEqual(self.product.get_discounted_price(20),80)    
        self.assertEqual(self.product.get_discounted_price(50),50)    
        self.assertEqual(self.product.get_discounted_price(0),100)  



    def test_negative_price_contraint(self):
        """ To test that a product with a negative price cannot be saved due to the databse constraints """
        
        with self.assertRaises(IntegrityError):

            self.negProduct.save()

    def test_negative_stock_count_contraint(self):
        """ To test that a product with a negative stock_count cannot be saved due to the databse constraints """
        self.negProduct.stock_count=-5
        self.negProduct.price = 2.00
        
        with self.assertRaises(IntegrityError):

            self.negProduct.save()





""" 
    def test_negative_price_validation(self):
        self.product.price = -10

        with self.assertRaises(ValidationError):
            self.product.clean()
 """
""" 
    def test_negative_stock_count_validation(self):
        self.product.stock_count = -10

        with self.assertRaises(ValidationError):
            self.product.clean()
 """            
