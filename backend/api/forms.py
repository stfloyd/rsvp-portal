from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse, reverse_lazy

from .models import User


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')


class UserCreationForm(forms.ModelForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'is_staff', 'is_superuser')
        widgets = {
            'password': forms.PasswordInput()
        }

