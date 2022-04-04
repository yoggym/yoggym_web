# Generated by Django 3.0.8 on 2020-10-03 20:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0021_tranferrequestform_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentform',
            name='subData',
        ),
        migrations.AddField(
            model_name='clientsubscriptionform',
            name='paymentId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.PaymentForm'),
        ),
        migrations.AddField(
            model_name='paymentform',
            name='gymId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.GymProfileForm'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentform',
            name='userId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tranferrequestform',
            name='subId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.ClientSubscriptionForm'),
            preserve_default=False,
        ),
    ]
