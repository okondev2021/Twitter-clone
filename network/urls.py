
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("Profile/<str:user>", views.profile, name="profile"),


    # API ROUTE
    path("like/<int:like_id>", views.post_like, name="like"),
    path("edit/<int:edit_id>", views.edit, name="edit")
]
