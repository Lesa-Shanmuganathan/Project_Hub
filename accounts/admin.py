from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'department', 'year', 'is_active']
    list_filter = ['role', 'department', 'year', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'department', 'year', 'roll_number', 
                      'profile_picture', 'bio', 'github_profile', 'linkedin_profile')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'department', 'year', 'roll_number')
        }),
    )
