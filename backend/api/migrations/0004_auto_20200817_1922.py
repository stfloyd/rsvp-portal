# Generated by Django 3.1 on 2020-08-17 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_event_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestGradeLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, verbose_name='name')),
                ('max_occupancy', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='guest',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.guestgradelevel'),
        ),
    ]
