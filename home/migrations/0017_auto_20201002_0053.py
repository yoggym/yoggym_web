# Generated by Django 3.0.8 on 2020-10-01 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_paymentform'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentform',
            name='gymId',
        ),
        migrations.RemoveField(
            model_name='paymentform',
            name='userId',
        ),
    ]
