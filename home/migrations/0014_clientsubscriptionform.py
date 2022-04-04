# Generated by Django 3.0.8 on 2020-10-01 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0013_auto_20200930_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientSubscriptionForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateTimeField()),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('plan', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('gymId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.ProfileMaster')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]