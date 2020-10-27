from django.db import models
from django.core.validators import MinLengthValidator, int_list_validator
# Create your models here.

class Fellow(models.Model):
    name = models.CharField(max_length=64)
    CNIC = models.CharField(max_length=13, 
        validators=[int_list_validator(sep=''),MinLengthValidator(13),])
    program = models.CharField(max_length=30)
    ID =  models.CharField(max_length=5)
    graduation = models.CharField(max_length=25)
    def __str__(self):
        return f"{self.name}"

class FellowAdmin (admin.ModelAdmin):
    search_fields = ('Name', 'CNIC', 'Program', 'ID', 'Graduation', )

admin.site.register (Fellow, FellowAdmin)