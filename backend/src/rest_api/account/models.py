from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone

class UserManager(BaseUserManager):
    # Creates and saves a User with the given email and password.
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        if not username:
            raise ValueError("The Username must be set")
        if not password:
            raise ValueError("The Password must be set")
        
        user = self.model(
            self.normalize_email(email),
            username = username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(email, username, password, extra_fields)
        user.is_staff()
        user.is_superuser = True
        user.save()
        return user

# Create your models here.
