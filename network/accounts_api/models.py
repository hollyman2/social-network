from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager


class Account(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_("email"), unique=True, max_length=254)
    password = models.CharField(_("password"), max_length=100)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

class ApiKey(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    
