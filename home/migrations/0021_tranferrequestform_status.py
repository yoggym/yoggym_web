# Generated by Django 3.0.8 on 2020-10-03 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_tranferrequestform'),
    ]

    operations = [
        migrations.AddField(
            model_name='tranferrequestform',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
