# Generated by Django 3.0.8 on 2020-12-16 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_bannerandroid'),
    ]

    operations = [
        migrations.CreateModel(
            name='OurServicesImagesAndroid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.FileField(upload_to='')),
            ],
        ),
    ]
