from django.urls import path
from .views import user_list, user_detail,all_posts, RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', user_list, name='users'),
    path('users/<uuid:id>/', user_detail, name='user-detail'),
    path('posts/', all_posts, name='posts'),
]
