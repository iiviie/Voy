# Generated by Django 5.1.3 on 2024-11-27 18:08

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15, verbose_name='phone number')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('email_verified', models.BooleanField(default=False)),
                ('phone_verified', models.BooleanField(default=False)),
                ('registration_pending', models.BooleanField(default=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='profile_photos/')),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], max_length=10, null=True)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('drivers_license_image', models.ImageField(blank=True, null=True, upload_to='drivers_licenses/')),
                ('is_driver_verified', models.BooleanField(default=False)),
                ('is_driver', models.BooleanField(default=False)),
                ('current_role', models.CharField(choices=[('DRIVER', 'Driver'), ('PASSENGER', 'Passenger')], default='PASSENGER', max_length=10)),
                ('rating_as_driver', models.FloatField(default=0.0)),
                ('rating_as_passenger', models.FloatField(default=0.0)),
                ('vehicle_number', models.CharField(blank=True, max_length=20, null=True)),
                ('vehicle_model', models.CharField(blank=True, max_length=50, null=True)),
                ('completed_rides_as_driver', models.IntegerField(default=0)),
                ('completed_rides_as_passenger', models.IntegerField(default=0)),
                ('total_seats', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('attempts', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('EMAIL', 'Email'), ('PASSWORD_RESET', 'password_reset'), ('PHONE', 'Phone')], default='EMAIL', max_length=20)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='otp_codes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(condition=models.Q(('registration_pending', False)), fields=('email',), name='unique_verified_email'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(condition=models.Q(('registration_pending', False)), fields=('phone_number',), name='unique_verified_phone'),
        ),
    ]
