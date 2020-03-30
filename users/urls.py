from django.urls import path
from .views import user_login_view, home_view, user_register_view, user_logout_view

app_name = 'users'
urlpatterns = [
  path('', home_view, name='home'),
  path('accounts/login/', user_login_view, name='login'),
  path('accounts/register/', user_register_view, name='register'),
  path('accounts/logout/', user_logout_view, name='logout'),
]