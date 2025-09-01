from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address
from django.utils.html import format_html


class AddressInline(admin.StackedInline):
    model = Address
    can_delete = False
    verbose_name_plural = 'Address'


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'profile_picture_preview', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('user_type', 'profile_picture', 'profile_picture_preview')
        }),
    )
    
    inlines = (AddressInline,)
    
    readonly_fields = ('profile_picture_preview',)
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_picture.url)
        return "No Image"
    profile_picture_preview.short_description = 'Profile Picture'


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'line1', 'city', 'state', 'pincode')
    list_filter = ('city', 'state')
    search_fields = ('user__username', 'user__email', 'line1', 'city', 'pincode')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Address, AddressAdmin)