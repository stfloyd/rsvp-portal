# Generated by Django 3.1 on 2020-08-18 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_guestgrade_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guestgrade',
            name='event',
        ),
    ]
