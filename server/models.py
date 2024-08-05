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
    # Use JSONField from django.db.models
    permissions = JSONField(default=dict, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Company(models.Model):

    COMPANY_ADDRESS_COUNTRY_SUBENTITY_CODE_CHOICES = (
        (1, 'RO-AB'), (2, 'RO-AR'), (3, 'RO-AG'), (4,'RO-BC'), (5, 'RO-BH'), (6, 'RO-BN'), (7, 'RO-BT'),
        (8, 'RO-BV'), (9, 'RO-BR'), (10, 'RO-BZ'), (11,'RO-CS'), (12, 'RO-CJ'), (13, 'RO-CT'), (14, 'RO-CV'),
        (15, 'RO-DB'), (16, 'RO-DJ'), (17, 'RO-GL'), (18,'RO-GJ'), (19, 'RO-HR'), (20, 'RO-HD'), (21, 'RO-IL'),
        (22, 'RO-IS'), (23, 'RO-IF'), (24, 'RO-MM'), (25,'RO-MH'), (26, 'RO-MS'), (27, 'RO-NT'), (28, 'RO-OT'),
        (29, 'RO-PH'), (30, 'RO-SM'), (31, 'RO-SJ'), (32,'RO-SB'), (33, 'RO-SV'), (34, 'RO-TR'), (35, 'RO-TM'),
        (36, 'RO-TL'), (37, 'RO-VS'), (38, 'RO-VL'), (39, 'RO-VN'), (40, 'RO-B'), (51, 'RO-CL'), (52, 'RO-GR'))

    company_name = models.CharField(max_length=100, null=False, blank=False)
    company_tin = models.IntegerField(null=False, blank=False)
    company_registration_number = models.PositiveIntegerField(
        null=False, blank=False)
    company_address_country = models.CharField(
        max_length=100, null=False, blank=False)
    company_address_country_code = models.CharField(
        max_length=100, null=False, blank=False)
    company_address_country_subentity = models.CharField(
        max_length=100, null=False, blank=False)
    company_address_country_subentity_code = models.PositiveIntegerField(
        max_length=100, choices=COMPANY_ADDRESS_COUNTRY_SUBENTITY_CODE_CHOICES, null=False, blank=False)
    company_address_city = models.CharField(
        max_length=100, null=False, blank=False)
    company_address_street = models.CharField(
        max_length=100, null=False, blank=False)
    company_address_details = models.CharField(
        max_length=100, null=False, blank=False)
    company_vat_status = models.CharField(
        max_length=100, null=False, blank=False)
    company_vat_number = models.PositiveIntegerField(null=False, blank=False)
