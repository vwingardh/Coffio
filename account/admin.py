from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from account.models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    password_1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Password confirmation', 
        widget=forms.PasswordInput
    )

    class Meta: 
        model = CustomUser
        fields = (
            'email', 
            'username', 
            'first_name', 
            'last_name', 
            'password'
        )

    def clean_password_2(self):
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")
        if password_1 and password_2 and password_1 != password_2:
            raise ValidationError("Passwords do not match.")
        return password_2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password_1"])
        if commit: 
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    form = UserRegistrationForm
    list_display = (
        'email', 
        'username', 
        'first_name', 
        'last_name', 
        'password'
    )
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
