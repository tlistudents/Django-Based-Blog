from django.db import models
from django.contrib.auth.models import User


# user info
class Profile(models.Model):
    # user and model is one to one relation
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # phone number
    phone = models.CharField(max_length=20, blank=True)
    # avatar
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # bio
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)
