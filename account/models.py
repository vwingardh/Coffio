from django_countries.fields import CountryField

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password):
        """
        Creates and saves a User with the required fields.
        """
        if not email:
            raise ValueError('Users must have an email address.')
        if not username:
            raise ValueError('Users must have a username.')
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            username=username, 
            first_name=first_name,
            last_name=last_name,
            password=password, 
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        """
        Creates and saves a superuser with the required fields.
        """      
        user = self.model(
            email=email, 
            username=username, 
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True, 
        verbose_name='email address', 
        max_length=255, 
        blank=False
    )
    username = models.CharField(
        max_length=150,
        unique=True, 
        blank=False
    )
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    phone_number = models.CharField(max_length=15, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    country = CountryField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_emails = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'email', 
        'first_name', 
        'last_name',
    ]

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"  
