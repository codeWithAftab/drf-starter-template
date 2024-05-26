from django.contrib import admin
from .models import *


@admin.register(CustomErrors)
class CustomErrorAdmin(admin.ModelAdmin):
    list_display = ('code', 'detail')
    