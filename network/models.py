from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Follow(models.Model):
    useradmin = models.IntegerField()
    follow = models.ForeignKey("User",on_delete=models.CASCADE, related_name="userfollow")

class Like(models.Model):
    post = models.ForeignKey("Posts", on_delete=models.CASCADE, related_name="postlike")
    like = models.ForeignKey("User",on_delete=models.CASCADE, related_name="userlike")

class Posts(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)

    def serialize(self):
        return {
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
