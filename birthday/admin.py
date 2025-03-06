from django.contrib import admin
from .models import Staff, User, NotificationTemplate, NotificationLog
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

class StaffInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        if not Staff.objects.filter(email=self.instance.email).exists():
            if not hasattr(self.instance, 'staff_profile'):
                # No linked Staff record was found.
                raise ValidationError(
                    "Admin users must be added as staff first."
                    "Please create the corresponding Staff record in the Staff table before adding this admin user."
                )

class StaffInline(admin.StackedInline):
    model = Staff
    formset = StaffInlineFormset
    extra = 0
    max_num = 1

    def has_add_permission(self, request, obj):
        if obj is None:
            return False
        
        if obj.is_staff and not obj.is_superuser:
            if not hasattr(obj, 'staff_profile'):
                return False
        
        return super().has_add_permission(request, obj)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Staff._meta.fields]
    fields = [field.name for field in Staff._meta.fields if field.name not in ["id", "created_at", "updated_at"]]



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Determines which fields will be shown in the list view of the Staff records in the admin interface.
    list_display = [field.name for field in User._meta.fields]
    # Specifies which fields should appear on the form when you add or edit a Staff record in the admin.
    fields = [field.name for field in User._meta.fields if field.name not in ["id", "created_at", "updated_at","username","first_name","last_name"]]
    inlines = [StaffInline]

    def save_model(self, request, obj, form, change):
        """Hashes the password before saving the user."""
        if form.cleaned_data.get("password"):  
            obj.set_password(form.cleaned_data["password"]) 
        super().save_model(request, obj, form, change)  

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NotificationTemplate._meta.fields]
    fields = [field.name for field in NotificationTemplate._meta.fields if field.name not in ["id", "created_at", "updated_at"]]

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NotificationLog._meta.fields]
    fields = [field.name for field in NotificationLog._meta.fields if field.name not in ["id","created_at"]]