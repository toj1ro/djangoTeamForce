from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.redirect_view, name="redirect"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("homepage", views.home_page, name="homepage"),
    path('profile/', views.profile, name='users-profile'),
    path('autoc/', views.autocmplete, name='autocomplete')
]
