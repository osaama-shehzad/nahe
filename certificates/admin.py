from django.contrib import admin

from .models import Fellow, FellowAdmin

# Register your models here.
#register
admin.site.register (Fellow, FellowAdmin)