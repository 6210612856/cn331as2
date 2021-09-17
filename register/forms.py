from django import forms
from django.db.models import fields
from .models import *


class ImageForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta :
        model = Student
        fields = ('image', 'title')