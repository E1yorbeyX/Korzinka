from django.contrib import admin
from .models import CustomUser, Shop, Cart, Category, Commet
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id', 'email', 'first_name', 'last_name')
    search_fields = ('email',)
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2', 'first_name', 'last_name')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Shop)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Commet)
