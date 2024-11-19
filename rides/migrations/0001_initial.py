# Generated by Django 5.1.3 on 2024-11-18 17:30

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
                'ordering': ['-created_at'],
            },
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
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled'), ('REJECTED', 'Rejected')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Passenger_ride_requests', to=settings.AUTH_USER_MODEL)),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='rides.ridedetails')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
