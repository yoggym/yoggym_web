# Generated by Django 3.0.8 on 2020-12-13 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_auto_20201127_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='bannerAndroid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.FileField(upload_to='')),
            ],
        ),
    ]