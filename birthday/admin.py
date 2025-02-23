from django.contrib import admin
from .models import Staff, User


@admin.register(Staff)
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Staff._meta.fields]
    fields = [field.name for field in Staff._meta.fields if field.name not in ["id", "created_at", "updated_at"]]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Determines which fields will be shown in the list view of the Staff records in the admin interface.
    list_display = [field.name for field in User._meta.fields]
    # Specifies which fields should appear on the form when you add or edit a Staff record in the admin.
    fields = [field.name for field in User._meta.fields if field.name not in ["id", "created_at", "updated_at"]]

    def save_model(self, request, obj, form, change):
        """Hashes the password before saving the user."""
        if form.cleaned_data.get("password"):  
            obj.set_password(form.cleaned_data["password"]) 
        super().save_model(request, obj, form, change)  

