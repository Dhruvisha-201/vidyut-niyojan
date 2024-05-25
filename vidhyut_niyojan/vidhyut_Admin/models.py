from django.db import models

# Create your models here.

class admin(models.Model):
    UserName = models.CharField(max_length=100)
    First_name = models.CharField(max_length=100)
    Password = models.CharField(max_length=10)
    Email = models.EmailField()
    Contact_no = models.CharField(max_length=12)


class Job_fair(models.Model):
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    opening_for = models.CharField(max_length=255)
    reqiured_Skill = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_cureentdate =models.DateField()
    IsActive = models.IntegerField()
    IsDeleted = models.BooleanField()