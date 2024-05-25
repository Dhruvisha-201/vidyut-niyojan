# Generated by Django 4.1.4 on 2022-12-29 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Candidate_Master', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_education_detail',
            name='Candidate_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Candidate_Master.candidate_register'),
        ),
        migrations.AlterField(
            model_name='candidate_experience',
            name='Candidate_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Candidate_Master.candidate_register'),
        ),
        migrations.AlterField(
            model_name='candidate_family_detail',
            name='Candidate_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Candidate_Master.candidate_register'),
        ),
        migrations.AlterField(
            model_name='candidate_personal_detail',
            name='Candidate_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Candidate_Master.candidate_register'),
        ),
        migrations.AlterField(
            model_name='candidate_skills',
            name='Candidate_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Candidate_Master.candidate_register'),
        ),
    ]
