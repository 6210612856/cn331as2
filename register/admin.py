from django.contrib import admin

# Register your models here.

from .models import *

class studentAdmin(admin.ModelAdmin):
    filter_horizontal = ("subject",)

admin.site.register(Subject)
admin.site.register(Student,studentAdmin)
