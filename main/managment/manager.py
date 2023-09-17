from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None , **kwargs):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    

    
    def create_superuser(self, email, password , **kwargs):
        kwargs.setdefault('is_staff' , True)
        kwargs.setdefault('is_superuser' , True)
        kwargs.setdefault('is_active' , True)
        
        if kwargs.get('is_staff') is not True:
            raise ValueError('Super User Must Have Staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Super User Must Have superuser=True') 
        return self.create_user(email,password,**kwargs)
