# Generated by Django 3.1 on 2020-08-17 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200817_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestgrade',
            name='registration',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='guest_grades', to='api.registration'),
            preserve_default=False,
        ),
    ]
