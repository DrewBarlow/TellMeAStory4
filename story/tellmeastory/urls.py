from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "tellmeastory"
urlpatterns = [
    path("", views.register, name="register"),
    path("index/", views.index, name="index"),
    path("account/<str:username>/", views.account, name="account_page"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("map/" , views.map , name="map") ,
    path("addtags/", include("managetags.urls")),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("addtags/", include("managetags.urls")),
    path("addnodeimage/", views.add_image, name="add_node_image"),
    path("create-story/", views.create_node, name="create_story"),
    path("author-story/<str:username>/", views.author_story, name="author_story"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
