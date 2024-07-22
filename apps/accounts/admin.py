from django.contrib import admin
from .models import CustomUser, StaffManager, StaffMember
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("uuid", 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ( 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'image', "uuid")}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'role')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ["uuid", "created_on"]

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'weekly_off')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    list_filter = ('user__role',)