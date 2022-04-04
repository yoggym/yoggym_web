# Generated by Django 3.2 on 2021-07-08 14:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_referralids_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='amount',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='wallet',
            name='lastWithdraw',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wallet',
            name='withdrawAmount',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]