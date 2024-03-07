from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_post, name='add_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('', views.all_posts, name='posts'),
]
