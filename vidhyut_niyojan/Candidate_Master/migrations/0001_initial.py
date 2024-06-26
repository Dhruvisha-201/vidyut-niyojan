# Generated by Django 4.1.4 on 2022-12-26 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('TrainingPartner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate_skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Skills_Name', models.CharField(max_length=30, null=True)),
                ('Candidate_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrainingPartner.candidatemaster')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate_register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_number', models.IntegerField()),
                ('FirstName', models.CharField(max_length=30)),
                ('LastName', models.CharField(max_length=30)),
                ('Candidate_Email', models.EmailField(max_length=254)),
                ('Candidate_password', models.CharField(max_length=15)),
                ('Phone_no', models.CharField(max_length=15)),
                ('DOB', models.DateField(default=False, null=True)),
                ('Address1', models.TextField(null=True)),
                ('Address2', models.TextField(null=True)),
                ('pincode', models.CharField(max_length=8, null=True)),
                ('Gender', models.CharField(max_length=10, null=True)),
                ('adhar_Number', models.IntegerField()),
                ('willing_to_relocate', models.CharField(max_length=50, null=True)),
                ('differently_abled', models.CharField(max_length=30)),
                ('Job_Name', models.CharField(max_length=50, null=True)),
                ('Training_Type', models.CharField(max_length=30, null=True)),
                ('Training_Status', models.CharField(max_length=30, null=True)),
                ('Placed_Status', models.CharField(max_length=30, null=True)),
                ('Qualification', models.CharField(max_length=50, null=True)),
                ('Training_Scheme_Name', models.CharField(max_length=30)),
                ('IsDeleted', models.IntegerField()),
                ('IsActive', models.BooleanField()),
                ('otp', models.IntegerField(blank=True, null=True)),
                ('otp_is_used', models.BooleanField(blank=True, null=True)),
                ('City_Id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TrainingPartner.citymaster')),
                ('Course_Id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TrainingPartner.courcemaster')),
                ('State_Id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TrainingPartner.statemaster')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate_personal_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_name', models.CharField(max_length=30, null=True)),
                ('Last_name', models.CharField(max_length=30)),
                ('Email', models.CharField(max_length=30)),
                ('Phone_number', models.IntegerField()),
                ('Address', models.TextField()),
                ('Current_Location', models.CharField(max_length=30)),
                ('Candidate_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrainingPartner.candidatemaster')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate_Family_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Father_Name', models.CharField(max_length=30, null=True)),
                ('Mother_Name', models.CharField(max_length=30, null=True)),
                ('Brother_Name', models.CharField(max_length=30, null=True)),
                ('Sister_Name', models.CharField(max_length=30, null=True)),
                ('Candidate_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrainingPartner.candidatemaster')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate_Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Total_Exp', models.IntegerField(null=True)),
                ('Objective', models.CharField(max_length=500, null=True)),
                ('Profile_Summary', models.CharField(max_length=100, null=True)),
                ('Company_Name', models.CharField(max_length=30, null=True)),
                ('Projects', models.CharField(max_length=200, null=True)),
                ('Candidate_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrainingPartner.candidatemaster')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate_education_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('University', models.CharField(max_length=30, null=True)),
                ('Passing_year', models.IntegerField(null=True)),
                ('Persentage', models.IntegerField(null=True)),
                ('Post_graduation', models.CharField(max_length=30, null=True)),
                ('Candidate_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrainingPartner.candidatemaster')),
            ],
        ),
    ]
