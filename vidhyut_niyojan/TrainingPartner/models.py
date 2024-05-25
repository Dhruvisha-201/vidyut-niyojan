from django.db import models

# Create your models here.


class Training_Partner(models.Model):
    Nsdc_Registration_Number = models.CharField(max_length=30)
    Training_Partner_Name = models.CharField(max_length=30)
    Legal_Entity_Name = models.CharField(max_length=30)
    Contact_Person_Name = models.CharField(max_length=30)
    Contact_Person_Email = models.EmailField()
    Password = models.CharField(max_length=30)
    Contact_Person_Phone = models.CharField(max_length=30)
    Alternate_Email = models.EmailField(null=True)
    Address = models.TextField()
    IsActive = models.IntegerField()
    IsDeleted = models.BooleanField()
    CreatedBy = models.CharField(max_length=30)
    CreatedDate = models.DateField()
    ModifiedBy =models.CharField(max_length=30)
    ModifiedDate = models.DateField()



class CountryMaster(models.Model):
    Country_Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Country_Name

class StateMaster(models.Model):
    country_Id = models.ForeignKey(CountryMaster, on_delete=models.CASCADE)
    State_Name = models.CharField(max_length=30)

    def __str__(self):
        return self.State_Name

class CityMaster(models.Model):
    State_Id = models.ForeignKey(StateMaster, on_delete=models.CASCADE)
    City_Name = models.CharField(max_length=30)

    def __str__(self):
        return self.City_Name


class Training_center(models.Model): 
    registerno = models.CharField(max_length=50)
    Training_Partner_Id = models.ForeignKey(Training_Partner, on_delete=models.CASCADE)
    state = models.ForeignKey(StateMaster, on_delete=models.CASCADE)
    City = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
    Training_Center_Name = models.CharField(max_length=30)
    Address1 = models.TextField()
    Address2 = models.TextField()
    Pin_Code = models.IntegerField()
    Contact_Name = models.CharField(max_length=30)
    Contact_Email = models.CharField(max_length=30)
    Password = models.CharField(max_length=15)
    Contact_No = models.CharField(max_length=15)
    IsDeleted = models.IntegerField()
    IsActive = models.IntegerField()
    CreatedBy = models.CharField(max_length=30)
    CreatedDate = models.DateField()
    ModifiedBy =models.CharField(max_length=30)
    ModifiedDate = models.DateField()

class CourceMaster(models.Model):
    Training_Center_Id = models.ForeignKey(Training_center, on_delete=models.CASCADE)
    CourseName = models.CharField(max_length=30)
    Duration = models.CharField(max_length=30)

    def __str__(self):
        return self.CourseName

class CandidateMaster(models.Model):
    Training_Partner_Id = models.ForeignKey(Training_Partner, on_delete=models.CASCADE, null=True)
    Training_Center_Id = models.ForeignKey(Training_center, on_delete=models.CASCADE, null=True)
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
    Job_role = models.CharField(max_length=30, null=True)
    Training_Type = models.CharField(max_length=30, null=True)
    Training_Status = models.CharField(max_length=30, null=True)
    Placed_Status = models.CharField(max_length=30, null=True)
    Qualification = models.CharField(max_length=50, null=True)
    Training_Scheme_Name = models.CharField(max_length=30)
    IsDeleted = models.IntegerField()
    IsActive = models.BooleanField()
    CreatedBy = models.CharField(max_length=30)
    CreatedDate = models.DateField()
    ModifiedBy =models.CharField(max_length=30)
    ModifiedDate = models.DateField()
    otp = models.IntegerField(null=True, blank=True) 
    otp_is_used = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.FirstName



class BatchMaster(models.Model):
    Course_Id = models.ForeignKey(CourceMaster, on_delete=models.CASCADE)
    Training_Center_Id = models.ForeignKey(Training_center, on_delete=models.CASCADE)
    StartDate = models.DateField()
    EndDate = models.DateField()
    WeekDays = models.CharField(max_length=300)
    Is_Closed = models.BooleanField()

class Candidate_batch(models.Model):
    Candidate_Id = models.ForeignKey(CandidateMaster, on_delete=models.CASCADE)
    Batch_Id = models.ForeignKey(BatchMaster, on_delete=models.CASCADE)
    Center_Id = models.ForeignKey(CourceMaster, on_delete=models.CASCADE)



class bulk_upload(models.Model):
    Training_Partner_Id = models.ForeignKey(Training_Partner, on_delete=models.CASCADE)
    Training_Center_Id = models.ForeignKey(Training_center, on_delete=models.CASCADE)
    bulk_upload_file = models.FileField()
    TotalRecord = models.IntegerField()
    TotalSkip = models.IntegerField()
    TotalSuccess = models.IntegerField()
    UploadedBy = models.CharField(max_length=30)
    UploadedDate = models.DateField()





