from django.urls import path
from .views import HomePage,Products,profile,login,posts

urlpatterns = [

    path('',HomePage,name='homepage'),
    path('products/',Products,name='products'),
    path('profile/',profile,name='profile'),
    path('login/',login,name='login'),
    path('post/',posts, name='post')
    
]
