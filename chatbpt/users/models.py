


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_paid = models.BooleanField(default=False)

class UserPreferences(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    theme = models.CharField(max_length=20, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"