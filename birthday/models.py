from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.functions import Lower
import uuid



class StaffType(models.TextChoices):
    Academic = "Academic"
    Non_Academic = "Non_Academic"

class Department(models.TextChoices):
    Botany = "Botany"
    Computer_Science ="Computer_Science"
    Chemistry = "Chemistry"
    Cell_Biology_And_Genetics = "Cell_Biology_And_Genetics"
    Marine_Sciences = "Marine_Sciences"
    Mathematics = "Mathematics"
    Microbiology = "Microbiology"
    Physics = "Physics"
    Statistics = "Statistics"
    Zoology = "Zoology"

class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    def __str__(self):
        return self.username
    
class Staff(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff_number = models.CharField(max_length=9, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                name='unique_lower_email'
            )
        ]

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower() 
        super().save(*args, **kwargs)

    phone_number = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^\d{11}$', message="Phone number must be exactly 11 digits.")], unique=True
    )
    department = models.CharField(
        max_length=100,
        choices=Department.choices,
        default=Department.Computer_Science
    )
    staff_type = models.CharField(
        max_length=100,
        choices=StaffType.choices,
        default=StaffType.Academic
    )
    profile_image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Birthday(models.Model):
    """
    Stores a single 'Birthday' entry, related to a Django user who 'owns' the birthday
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    staff = models.OneToOneField(
    Staff,
    on_delete=models.CASCADE,
    related_name='birthday',
)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date_of_birth}"