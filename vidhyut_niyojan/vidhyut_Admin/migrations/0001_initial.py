# Generated by Django 4.1.4 on 2022-12-26 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserName', models.CharField(max_length=100)),
                ('First_name', models.CharField(max_length=100)),
                ('Password', models.CharField(max_length=10)),
                ('Email', models.EmailField(max_length=254)),
                ('Contact_no', models.CharField(max_length=12)),
            ],
        ),
    ]