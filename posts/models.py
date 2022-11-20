from tkinter import CASCADE
from unicodedata import category, name
from django.db import models
from django.db.models import CharField, TextField, IntegerField
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name=CharField(max_length=100)


class Job(models.Model):
    company=CharField(max_length=100)
    post=CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.RESTRICT)
    location=CharField(max_length=50)
    details=TextField()
    deadline = models.DateField()
    applicants = models.ManyToManyField(User, through="UserJob")
    user_id = IntegerField()


class UserJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='./', verbose_name="cv")


class Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    type = models.CharField(max_length=100, default="individual")