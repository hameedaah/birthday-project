from django.db import models
import uuid
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser



class StaffType(models.TextChoices):
    Academic = "Academic"
    Non_Academic = "Non_Academic"

class Department(models.TextChoices):
    Computer_Science ="Computer_Science"

class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    department = models.CharField(choices=Department, default=Department.Computer_Science, max_length=100)
    staff_type = models.CharField(choices=StaffType, default=StaffType.Academic, max_length=100)
    # is_admin = models.BooleanField(default=False)
    # You can add any additional fields here if needed, for example:
    # phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username



class Birthday(models.Model):
    """
    Stores a single 'Birthday' entry, related to a Django user who 'owns' the birthday
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='birthdays'
    )
    birth_date = models.DateField()


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.birth_date}"
