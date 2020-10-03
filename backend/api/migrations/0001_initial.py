# Generated by Django 3.1 on 2020-08-12 14:43

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
            ],
            options={
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('max_occupancy', models.IntegerField(blank=True, null=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('open', models.DateTimeField()),
                ('close', models.DateTimeField()),
                ('show', models.DateTimeField(blank=True, null=True)),
                ('hide', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'event',
            },
        ),
        migrations.CreateModel(
            name='EventLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('max_occupancy', models.IntegerField()),
            ],
            options={
                'db_table': 'event_location',
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('variant', models.IntegerField(choices=[(None, '(Unknown)'), (0, 'Child'), (1, 'Adult')])),
                ('grade', models.IntegerField(choices=[(None, '(Unknown)'), (0, 'Nursery'), (1, 'Kindergarten')], null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'guest',
            },
        ),
        migrations.CreateModel(
            name='GuestAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'guest_attendance',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'host',
            },
        ),
        migrations.CreateModel(
            name='PreRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'preregistration',
            },
        ),
        migrations.CreateModel(
            name='HostAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.event')),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.host')),
            ],
            options={
                'db_table': 'host_attendance',
            },
        ),
        migrations.AddConstraint(
            model_name='host',
            constraint=models.UniqueConstraint(fields=('first_name', 'last_name', 'email'), name='unique_host'),
        ),
        migrations.AddField(
            model_name='guestattendance',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.event'),
        ),
        migrations.AddField(
            model_name='guestattendance',
            name='guest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.guest'),
        ),
        migrations.AddField(
            model_name='guest',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guests', to='api.host'),
        ),
        migrations.AddField(
            model_name='eventlocation',
            name='preregistration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_locations', to='api.preregistration'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.eventlocation'),
        ),
        migrations.AddField(
            model_name='event',
            name='preregistration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='api.preregistration'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='hostattendance',
            constraint=models.UniqueConstraint(fields=('event', 'host'), name='unique_host_attendance'),
        ),
        migrations.AddConstraint(
            model_name='guestattendance',
            constraint=models.UniqueConstraint(fields=('event', 'guest'), name='unique_guest_attendance'),
        ),
        migrations.AddConstraint(
            model_name='guest',
            constraint=models.UniqueConstraint(fields=('first_name', 'last_name', 'host'), name='unique_guest'),
        ),
    ]
