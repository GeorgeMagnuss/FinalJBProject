from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, Country, Vacation, Like


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_name']
    search_fields = ['role_name']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_name']
    search_fields = ['country_name']
    ordering = ['country_name']


@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ['country', 'description', 'start_date', 'end_date', 'price', 'like_count']
    list_filter = ['country', 'start_date']
    search_fields = ['country__country_name', 'description']
    ordering = ['start_date']
    
    def like_count(self, obj):
        return obj.like_count
    like_count.short_description = 'Likes'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'vacation']
    list_filter = ['vacation__country']
    search_fields = ['user__email', 'vacation__country__country_name']
