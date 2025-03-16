

from django import forms
from .models import CustomUser, UserPreferences

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'is_paid']


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = ['theme', 'notifications_enabled']