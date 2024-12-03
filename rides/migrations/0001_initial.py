# Generated by Django 5.1.3 on 2024-12-03 06:14

import django.contrib.gis.db.models.fields
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RideDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_location', models.CharField(max_length=255)),
                ('end_location', models.CharField(max_length=255)),
                ('start_point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('end_point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('route_line', django.contrib.gis.db.models.fields.LineStringField(blank=True, null=True, srid=4326)),
                ('start_time', models.DateTimeField()),
                ('available_seats', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ONGOING', 'Ongoing'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_rides', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ride Detail',
                'verbose_name_plural': 'Ride Details',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_given', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_received', to=settings.AUTH_USER_MODEL)),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.ridedetails')),
            ],
        ),
        migrations.CreateModel(
            name='PassengerRideRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=255)),
                ('dropoff_location', models.CharField(max_length=255)),
                ('pickup_point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('dropoff_point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('seats_needed', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled'), ('REJECTED', 'Rejected'), ('IN_VEHICLE', 'In Vehicle'), ('COMPLETED', 'Completed')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment_completed', models.BooleanField(default=False, null=True)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Passenger_ride_requests', to=settings.AUTH_USER_MODEL)),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='rides.ridedetails')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.ridedetails')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='ridedetails',
            index=models.Index(fields=['status', 'start_time'], name='rides_rided_status_5c76ee_idx'),
        ),
        migrations.AddIndex(
            model_name='ridedetails',
            index=models.Index(fields=['driver', 'status'], name='rides_rided_driver__6ebd0d_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('ride', 'from_user', 'to_user')},
        ),
        migrations.AddIndex(
            model_name='passengerriderequest',
            index=models.Index(fields=['status', 'ride'], name='rides_passe_status_f6a5f1_idx'),
        ),
        migrations.AddIndex(
            model_name='passengerriderequest',
            index=models.Index(fields=['passenger', 'status'], name='rides_passe_passeng_3f401a_idx'),
        ),
    ]
