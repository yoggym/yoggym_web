# Generated by Django 3.0.8 on 2020-10-01 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_paymentform_subdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientsubscriptionform',
            name='gymId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.GymProfileForm'),
        ),
    ]
