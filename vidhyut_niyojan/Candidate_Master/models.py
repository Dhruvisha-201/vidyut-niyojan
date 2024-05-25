from django.db import models
from TrainingPartner.models import *

# Create your models here.


class Candidate_register(models.Model):
    certificate_number = models.IntegerField()
    City_Id = models.ForeignKey(CityMaster, on_delete=models.CASCADE, null=True)
    State_Id = models.ForeignKey(StateMaster, on_delete=models.CASCADE, null=True)
    Course_Id = models.ForeignKey(CourceMaster, on_delete=models.CASCADE, null=True)
    FirstName = models.CharField(max_length=30)
    LastName = models.CharField(max_length=30)
    Candidate_Email = models.EmailField()
    Candidate_password = models.CharField(max_length=15)
    Phone_no = models.CharField(max_length=15)
    DOB = models.DateField(auto_now_add=False, default=False, null=True)
    Address1 = models.TextField(null=True)
    Address2 = models.TextField(null=True)
    pincode = models.CharField(max_length=8, null=True)
    Gender = models.CharField(max_length=10, null=True)
    adhar_Number = models.IntegerField()
    willing_to_relocate = models.CharField(max_length=50, null=True)
    differently_abled = models.CharField(max_length=30)
    Job_Name = models.CharField(max_length=50, null=True)
    Training_Type = models.CharField(max_length=30, null=True)
    Training_Status = models.CharField(max_length=30, null=True)
    Placed_Status = models.CharField(max_length=30, null=True)
    Qualification = models.CharField(max_length=50, null=True)
    Training_Scheme_Name = models.CharField(max_length=30)
    IsDeleted = models.IntegerField()
    IsActive = models.BooleanField()
    otp = models.IntegerField(null=True, blank=True) 
    otp_is_used = models.BooleanField(null=True, blank=True)


class Candidate_personal_detail(models.Model):
    Candidate_Id = models.ForeignKey(Candidate_register, on_delete=models.CASCADE)
    First_name = models.CharField(max_length=30, null=True)
    Last_name = models.CharField(max_length=30)
    Email = models.CharField(max_length=30)
    Phone_number = models.IntegerField()
    Address = models.TextField()
    Current_Location = models.CharField(max_length=30)
    

class Candidate_skills(models.Model):
    Candidate_Id = models.ForeignKey(Candidate_register, on_delete=models.CASCADE)
    Skills_Name = models.CharField(max_length=30, null=True)


class Candidate_education_detail(models.Model):
    Candidate_Id = models.ForeignKey(Candidate_register, on_delete=models.CASCADE)
    University = models.CharField(max_length=30, null=True)
    Passing_year = models.IntegerField(null=True)
    Persentage = models.IntegerField(null=True)
    Post_graduation = models.CharField(max_length=30, null=True)

class Candidate_Family_Detail(models.Model):
    Candidate_Id = models.ForeignKey(Candidate_register, on_delete=models.CASCADE)
    Father_Name = models.CharField(max_length=30, null=True)
    Mother_Name = models.CharField(max_length=30, null=True)
    Brother_Name = models.CharField(max_length=30, null=True)
    Sister_Name = models.CharField(max_length=30, null=True)

class Candidate_Experience(models.Model):
    Candidate_Id = models.ForeignKey(Candidate_register, on_delete=models.CASCADE)
    Total_Exp = models.IntegerField(null=True)
    Objective = models.CharField(max_length=500, null=True)
    Profile_Summary = models.CharField(max_length=100, null=True)
    Company_Name = models.CharField(max_length=30, null=True)
    Projects = models.CharField(max_length=200, null=True)