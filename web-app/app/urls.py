from django.urls import path
from .views import user_list, user_detail, register, login, all_posts, base

urlpatterns = [
    path('users/', user_list, name='users'),
    path('users/<uuid:id>/', user_detail, name='user-detail'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('posts/', all_posts, name='posts'),
    path('base/', base, name='base'),
]
