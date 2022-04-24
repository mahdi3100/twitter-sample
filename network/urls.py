
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("newpost", views.newpost, name="newpost"),
    path("editpost", views.editpost, name="editpost"),

    path("profile/<int:userid>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("like", views.like, name="like"),
    path("following", views.following, name="following"),



    #path("posts/<int:post_id>", views.email, name="email"),
    #path("posts/<int:getspost>", views.mailbox, name="mailbox")
]
