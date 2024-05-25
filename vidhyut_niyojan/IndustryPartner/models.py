from django.db import models
from  TrainingPartner.models import *
# Create your models here.

class Industry_partner(models.Model):
    registerno = models.CharField(max_length=50)
    First_Name = models.CharField(max_length=30)
    Last_name = models.CharField(max_length=30)
    Partner_Type = models.CharField(max_length=30)
    Legal_Entity_Name = models.CharField(max_length=30)
    SPOC_Name = models.CharField(max_length=30)
    SPOC_Email = models.EmailField()
    Password = models.CharField(max_length=30)
    SPOC_Phone = models.CharField(max_length=15)
    Full_Address = models.TextField()
    State_Name = models.ForeignKey("TrainingPartner.StateMaster", on_delete=models.CASCADE)
    District_Name = models.ForeignKey("TrainingPartner.CityMaster", on_delete=models.CASCADE)
    PIN_Code = models.CharField(max_length=8)
    Office_Phone_No = models.CharField(max_length=15)
    Website_Link = models.CharField(max_length=30)
    IsActive = models.IntegerField()
    IsDeleted = models.IntegerField()
    CreatedBy = models.CharField(max_length=30)
    CreatedDate = models.DateField()
    ModifiedBy = models.CharField(max_length=30)
    ModifiedDate = models.DateField()


class Partner_Type(models.Model):
    type_name = models.CharField(max_length=100)

    
class Job_Posting(models.Model):
    Job_Name = models.CharField(max_length=50)
    Job_type = models.CharField(max_length=50)
    Job_salary = models.IntegerField()
    Job_Description = models.TextField()
    Requirements = models.CharField(max_length=50)
    Number_Of_Requirements = models.IntegerField()
    Job_Add_Date = models.DateField(null=True,blank=True)
    Job_Ending_Date = models.DateField(null=True,blank=True)
    Experience = models.IntegerField()
    Qualification =models.CharField(max_length=200)
    Industry_partner_id = models.ForeignKey(Industry_partner, on_delete=models.CASCADE)
    Country_id = models.ForeignKey(CountryMaster, on_delete=models.CASCADE)
    State_id = models.ForeignKey(StateMaster, on_delete=models.CASCADE)
    City_id = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
    IsActive = models.IntegerField()
    IsDeleted = models.IntegerField()
    createby = models.CharField(max_length=30)
    CreatedDate = models.DateField()
    ModifiedBy = models.CharField(max_length=30)
    ModifiedDate = models.DateField()
    
class Hiring_Request(models.Model):
    candidate_id = models.ForeignKey(CandidateMaster, on_delete=models.CASCADE)
    Training_id = models.ForeignKey(Training_Partner, on_delete=models.CASCADE)
    Job_id = models.ForeignKey(Job_Posting, on_delete=models.CASCADE)
    IsActive = models.IntegerField()
    IsDeleted = models.IntegerField()
    createby = models.CharField(max_length=30)
    CreatedDate = models.DateField()
    ModifiedBy = models.CharField(max_length=30)
    ModifiedDate = models.DateField()
    
class Candidate_apply_job(models.Model):
    Candidate_Id = models.ForeignKey(CandidateMaster, on_delete=models.CASCADE)
    Trainingpartner_id = models.ForeignKey(Training_Partner, on_delete=models.CASCADE)
    CreatedBy = models.CharField(max_length=30)
    CreatedDate = models.DateField()
    ModifiedBy = models.CharField(max_length=30)
    ModifiedDate = models.DateField()


class Candidate_job_Status(models.Model):
    Candidate_Id = models.ForeignKey(CandidateMaster, on_delete=models.CASCADE)
    Job_Id  = models.ForeignKey(Job_Posting, on_delete=models.CASCADE)
    Job_status = models.CharField(max_length=30)


class RPL_Master(models.Model):
    Industry_partner_Id = models.ForeignKey(Industry_partner, on_delete=models.CASCADE)
    Trining_type = models.CharField(max_length=50)
    Target = models.IntegerField()
    Job_role = models.CharField(max_length=30)
    Area = models.CharField(max_length=30)
    Country_Id =models.ForeignKey(CountryMaster, on_delete=models.CASCADE)
    State_Id = models.ForeignKey(StateMaster, on_delete=models.CASCADE)
    City_Id = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
    pincode = models.IntegerField()
    SPOC_Name = models.CharField(max_length=30)
    SPOC_Number = models.CharField(max_length=12)
    SPOC_Email = models.EmailField()
    SPOC_Designation = models.CharField(max_length=30)
    Is_deleted = models.BooleanField()
    IsActive = models.BooleanField()