# server/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import JSONField  # Updated import

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_2fa_active = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='pending')
    creation_time = models.DateTimeField(auto_now_add=True)
    last_active_time = models.DateTimeField(auto_now=True)
    permissions = JSONField(default=dict, blank=True)  # Use JSONField from django.db.models

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    company_registration_number = models.CharField(max_length=50)
    company_tin = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255)
    company_address_country_subentity = models.CharField(max_length=100)
    company_address_country = models.CharField(max_length=100, default='Romania')
    company_address_country_code = models.CharField(max_length=10, default='RO')
    company_address_country_subentity_code = models.CharField(max_length=10)
    company_address_city = models.CharField(max_length=100)
    company_address_street = models.CharField(max_length=255)
    company_address_details = models.CharField(max_length=255, blank=True, null=True)
    company_vat_status = models.BooleanField(default=False)
    company_vat_number = models.CharField(max_length=50, blank=True, null=True)
    additional_info = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.company_name
