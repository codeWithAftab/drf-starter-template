from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from apps.accounts.managers import CustomUserManager
import uuid
from helper.id_generator import generate_employee_id
from helper.constant import USER_ROLES

def upload_profile_images(instance, filename):
    return f'accounts/{instance.uuid}/{filename}'

class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUser(BaseModel, AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=122, null=True, blank=True)
    first_name  = models.CharField(max_length=20, null=True, blank=True)
    last_name  = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    email = models.EmailField(verbose_name='email', unique=True)
    role = models.CharField(choices=USER_ROLES, max_length=122)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.uuid} - name: {self.first_name}"

  
class StaffMember(models.Model):
    employee_id = models.CharField(max_length=122, unique=True, default=generate_employee_id)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    weekly_off = models.JSONField(default=["saturday", "sunday"], null=True, blank=True)


class StaffManager(models.Model):
    employee_id = models.CharField(max_length=122, unique=True, default=generate_employee_id)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

