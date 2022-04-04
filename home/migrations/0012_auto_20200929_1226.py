# Generated by Django 3.0.8 on 2020-09-29 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20200929_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymprofileform',
            name='halfyearlyAbout',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='gymprofileform',
            name='halfyearlyPrice',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gymprofileform',
            name='monthlyAbout',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='gymprofileform',
            name='monthlyPrice',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gymprofileform',
            name='quarterlyAbout',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='gymprofileform',
            name='quarterlyPrice',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gymprofileform',
            name='yearlyAbout',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='gymprofileform',
            name='yearlyPrice',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]