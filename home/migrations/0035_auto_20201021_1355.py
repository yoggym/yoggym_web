# Generated by Django 3.0.8 on 2020-10-21 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_remove_gymfeatures_trainer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymprofileform',
            name='featuresId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.GymFeatures'),
        ),
    ]
