from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from apps.accounts.managers import CustomUserManager
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone


def upload_profile_images(instance, filename):
    # file will be uploaded to MEDIA_ROOT / audio/chapters/{reciter_name}/filename.mp3
    return f'accounts/{instance.uid}/{filename}'

def upload_cover_image(instance, filename):
    # file will be uploaded to MEDIA_ROOT / audio/chapters/{reciter_name}/filename.mp3
    return f'accounts/cover/{instance.uid}/{filename}'

class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class CustomUser(BaseModel, AbstractUser):
    uuid = models.CharField(max_length=255, default=uuid.uuid1)
    uid = models.CharField(max_length=255) # add unique=True
    username = models.CharField(verbose_name="username",max_length=122, unique=True, null=True,blank=True)
    image = models.ImageField(upload_to=upload_profile_images, blank=True, null=True)
    cover_image = models.ImageField(upload_to=upload_cover_image, null=True, blank=True)
    email = models.EmailField(verbose_name='email', unique=True)
    first_name  = models.CharField(max_length=20, null=True, blank=True)
    last_name  = models.CharField(max_length=20, null=True, blank=True)
    phone_number  = models.CharField(max_length=20, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    GENDERS = (
        ("male", "MALE"),
        ("female", "FEMALE"),
        ("other", "OTHER"),
    )
    gender = models.CharField(max_length=10, choices=GENDERS, null=True)
    address_line = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=6, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    country_code = models.IntegerField(default=91) # 91 for india.
    date_of_birth = models.DateField(null=True, blank=True)
    is_partner = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.uid} - name: {self.first_name}"



class Device(models.Model):
    users = models.ManyToManyField(CustomUser, related_name="devices")
    device_id = models.CharField(max_length=255, unique=True)
    is_logged_in = models.BooleanField(default=False)
    fcm_token = models.CharField(max_length=255, null=True, blank=True) # add unique=True
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.device_id)
    
    
    def logout(self):
        self.is_logged_in = False
        self.save()


    def login(self):
        self.is_logged_in = True
        self.save()


    def update_fcm_token(self, fcm_token):
        self.fcm_token = fcm_token
        self.save()


    def update_user(self, user):
        self.user = user
        self.save()

