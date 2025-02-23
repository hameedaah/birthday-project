from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError
from datetime import date
import uuid


class StaffType(models.TextChoices):
    academic = "academic"
    non_academic = "non_academic"

class NotificationType(models.TextChoices):
    email = "email"
    phone_number = "phone_number"

class Department(models.TextChoices):
    botany = "botany"
    computer_science ="computer_science"
    chemistry = "chemistry"
    cell_biology_and_genetics = "cell_biology_and_genetics"
    marine_sciences = "marine_sciences"
    mathematics = "mathematics"
    microbiology = "microbiology"
    physics = "physics"
    statistics = "statistics"
    zoology = "zoology"

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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^\d{11}$', message="Phone number must be exactly 11 digits.")], unique=True
    )
    department = models.CharField(
        max_length=100,
        choices=Department.choices,
        default=Department.computer_science
    )
    staff_type = models.CharField(
        max_length=100,
        choices=StaffType.choices,
        default=StaffType.academic
    )
    date_of_birth = models.DateField()
    profile_image_url = models.URLField(blank=True)
    notification_type = models.CharField(
        max_length=100,
        choices=NotificationType.choices,
        default=NotificationType.email
    )
    is_enabled = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                name='unique_lower_email'
            )
        ]
    
    def clean(self):
        if self.date_of_birth and self.date_of_birth > date.today():
            raise ValidationError({"date_of_birth": "Date of birth cannot be in the future."})

    def save(self, *args, **kwargs):
        self.full_clean()  
        if self.email:
            self.email = self.email.lower() 
        super().save(*args, **kwargs) 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
