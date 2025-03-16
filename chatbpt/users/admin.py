

from django.contrib import admin
from .models import CustomUser, UserPreferences

admin.site.register(CustomUser)
admin.site.register(UserPreferences)