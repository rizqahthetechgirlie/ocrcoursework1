

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields to display in the list view
    list_display = ("user_id", "username", "first_name", "last_name", "role", "email", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    # Organize fields into sections
    fieldsets = (
        (None, {"fields": ("password",)}),  # Exclude 'username' here
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "guardian_email", "year_group")}),
        ("Role Information", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields required when creating a user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "email", "password1", "password2", "role"),
            },
        ),
    )

    # Search and ordering
    search_fields = ("email", "first_name", "last_name", "role")
    ordering = ("user_id",)

    # Completely exclude 'username' from forms
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "username" in form.base_fields:
            del form.base_fields["username"]
        return form

# This registers the model and custom admin
admin.site.register(CustomUser, CustomUserAdmin)


