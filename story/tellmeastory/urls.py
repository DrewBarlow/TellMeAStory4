from django.urls import path
from . import views

app_name = "tellmeastory"
urlpatterns = [
    path("", views.index, name="index"),
    path("account/<str:username>", views.account, name="login"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
]
