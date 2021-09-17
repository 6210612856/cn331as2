from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subject(models.Model):
    subject_id = models.CharField(max_length=5 , primary_key= True)
    subject_name = models.CharField(max_length=64)
    semester = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    max_seat = models.PositiveIntegerField()
    available = models.BooleanField()
    
    def __str__(self) -> str:
         return f"{self.subject_id} ({self.subject_name})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject, blank=True, related_name="subject")
    title = models.CharField(max_length= 50 , default = "ayaya")
    img = models.ImageField(upload_to='images/uploads' , default = '/images/a.jpg')

    def __str__(self) -> str:
         return f"{self.user} "


