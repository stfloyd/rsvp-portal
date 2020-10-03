# Generated by Django 3.1 on 2020-08-17 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200817_2038'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PreRegistration',
            new_name='Registration',
        ),
        migrations.AlterModelOptions(
            name='registration',
            options={'verbose_name': 'Registration', 'verbose_name_plural': 'Registrations'},
        ),
        migrations.RenameField(
            model_name='event',
            old_name='preregistration',
            new_name='registration',
        ),
        migrations.RenameField(
            model_name='eventlocation',
            old_name='preregistration',
            new_name='registration',
        ),
        migrations.AlterModelTable(
            name='registration',
            table='registration',
        ),
    ]