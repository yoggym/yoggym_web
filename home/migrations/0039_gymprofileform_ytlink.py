# Generated by Django 3.0.8 on 2020-11-26 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_auto_20201127_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymprofileform',
            name='ytlink',
            field=models.CharField(default='https://www.youtube.com/watch?v=dYvr9RPfxlM', max_length=1000),
            preserve_default=False,
        ),
    ]
