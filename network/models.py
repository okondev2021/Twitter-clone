from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class POST(models.Model):
    USERNAME = models.ForeignKey('User',on_delete=models.CASCADE, related_name="userpost")
    POST = models.CharField(max_length = 10000)
    TIMESTAMP = models.DateTimeField(auto_now_add=True)
    LIKES = models.ManyToManyField("User", related_name="No_likes",blank=True)

    def __str__(self):
        return f"{self.id} :{self.USERNAME} posted: {self.POST}"

class USERPROFILE(models.Model):
    USERNAME = models.ForeignKey('User',on_delete=models.CASCADE, related_name="userprofile")
    FOLLOWERS = models.ManyToManyField("User", related_name="No_followers",blank=True)
    FOLLOWING = models.ManyToManyField("User", related_name="No_following",blank=True)

    def __str__(self):
        return f"Profile: {self.id} {self.USERNAME}"