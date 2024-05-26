from django.contrib import admin
from .models import CustomUser, Device
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ("uid", 'email', 'first_name', 'last_name', 'is_partner', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'gender', 'is_partner')
    fieldsets = (
        ("Auth Details", {'fields': ('email', 'password', "uid")}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'address_line', 'zip_code', 'country_code', 'gender', 'image', 'cover_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'is_logged_in', 'created_on', 'updated_on')
    list_filter = ('is_logged_in',)
    search_fields = ('device_id', 'users__email')
