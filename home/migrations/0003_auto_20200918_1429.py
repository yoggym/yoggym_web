# Generated by Django 3.0.8 on 2020-09-18 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200918_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientprofileform',
            name='height',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='clientprofileform',
            name='profilePic',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientprofileform',
            name='weight',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
