from django.contrib import admin

# Register your models here.
from .models import Birthday, User

@admin.register(Birthday)
class BirthdayAdmin(admin.ModelAdmin):
    list_display = ('birth_date', 'user', 'created_at', 'updated_at')
    list_filter = ('birth_date',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Dynamically gather all field names from the User model
    list_display = [field.name for field in User._meta.fields if field.name != "id"]

    # Optionally, if you also want to show all fields when editing a user in admin:
    fields = [field.name for field in User._meta.fields if field.name != "id"]