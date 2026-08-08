from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.coffee_list, name='coffee_list'),
    path('login/', auth_views.LoginView.as_view(template_name='coffee/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='coffee_list'), name='logout'),
]