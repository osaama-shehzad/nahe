from django.db import models
from django.core.validators import MinLengthValidator, int_list_validator
# Create your models here.

class Fellow(models.Model):
    name = models.CharField(max_length=64)
    CNIC = models.CharField(max_length=13, 
        validators=[int_list_validator(sep=''),MinLengthValidator(13),])
    program = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.name}"