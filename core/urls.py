from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
