from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager
from django.core.validators import FileExtensionValidator


class Account(AbstractBaseUser, PermissionsMixin):
    IMAGE_VALIDATOR = FileExtensionValidator(allowed_extensions=['JPG', 'JPEG'])

    email = models.EmailField(_("email"), unique=True, max_length=254)
    password = models.CharField(_("password"), max_length=100)
    first_name = models.CharField(_("first_name"), max_length=50)
    last_name = models.CharField(_("last_name"), max_length=50)
    login = models.CharField(_("login"), max_length=50, unique=True)
    phone = models.IntegerField()
    picture = models.ImageField(
        'Picture',
        upload_to='profiles_pictures/images/%Y/%m/%d/',
        validators=[IMAGE_VALIDATOR,],
        null=True,
        blank=True,
    )

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




