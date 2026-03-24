from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_verified', 'created_at')
    list_filter = ('is_active', 'is_staff', 'is_verified', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Verification', {'fields': ('is_verified',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'id')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'purpose', 'is_used', 'expires_at', 'created_at')
    list_filter = ('purpose', 'is_used', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'otp_code', 'purpose')}),
        ('Status', {'fields': ('is_used', 'failed_attempts')}),
        ('Timestamps', {'fields': ('expires_at', 'created_at')}),
    )
    
    readonly_fields = ('created_at', 'expires_at', 'id')
