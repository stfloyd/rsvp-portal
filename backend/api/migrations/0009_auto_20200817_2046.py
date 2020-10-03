# Generated by Django 3.1 on 2020-08-17 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_guestgrade_registration'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='guestgrade',
            constraint=models.UniqueConstraint(fields=('registration', 'name'), name='unique_grades'),
        ),
    ]
