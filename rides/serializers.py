from django.db.models import Q

from rest_framework import serializers
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from .models import RideDetails, PassengerRideRequest


class PointFieldSerializer(serializers.Field):
    def to_representation(self, value):
        if value is None:
            return None
        return {
            "type": "Point",
            "coordinates": [value.x, value.y]
        }

    def to_internal_value(self, data):
        try:
            if isinstance(data, dict):
                if data.get('type') != 'Point':
                    raise serializers.ValidationError("Only Point type is supported")
                coords = data.get('coordinates', [])
                if len(coords) != 2:
                    raise serializers.ValidationError("Invalid coordinates format")
                return Point(coords[0], coords[1], srid=4326)
            raise serializers.ValidationError("Invalid format")
        except (KeyError, ValueError, TypeError):
            raise serializers.ValidationError("Invalid Point format")

class RideDetailsSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField()
    start_point = PointFieldSerializer()
    end_point = PointFieldSerializer()
    
    class Meta:
        model = RideDetails
        fields = '__all__'
        read_only_fields = ['driver', 'status']

    def get_driver_name(self, obj):
        return obj.driver.get_full_name() or obj.driver.email

    def create(self, validated_data):
        validated_data['driver'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['start_point', 'end_point']:
            point = getattr(instance, field)
            if point:
                data[field] = {
                    'type': 'Point',
                    'coordinates': [point.x, point.y]
                }
        return {'success': True, 'data': data}

class RideRequestSerializer(serializers.ModelSerializer):
    passenger_name = serializers.SerializerMethodField()
    pickup_point = PointFieldSerializer()
    dropoff_point = PointFieldSerializer()
    
    class Meta:
        model = PassengerRideRequest
        fields = '__all__'
        read_only_fields = ['passenger', 'status']

    def get_passenger_name(self, obj):
        return obj.passenger.get_full_name() or obj.passenger.email

    def validate(self, data):
        ride = data['ride']
        seats = data.get('seats_needed', 1)
        
        if ride.status != 'PENDING':
            raise serializers.ValidationError("This ride is no longer accepting requests")
        
        if seats > ride.available_seats:
            raise serializers.ValidationError(f"Only {ride.available_seats} seats available")
        
        if PassengerRideRequest.objects.filter(
            passenger=self.context['request'].user,
            ride=ride,
            status='PENDING'
        ).exists():
            raise serializers.ValidationError("You already have a pending request for this ride")
            
        return data

    def create(self, validated_data):
        validated_data['passenger'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['pickup_point', 'dropoff_point']:
            point = getattr(instance, field)
            if point:
                data[field] = {
                    'type': 'Point',
                    'coordinates': [point.x, point.y]
                }
        return {'success': True, 'data': data}


class RideSearchSerializer(serializers.Serializer):
    pickup_point = PointFieldSerializer()
    destination_point = PointFieldSerializer()
    seats_needed = serializers.IntegerField(default=1, min_value=1, max_value=8)
    radius = serializers.FloatField(default=5000.0, min_value=0.0)

    def get_available_rides(self):
        data = self.validated_data
        return RideDetails.objects.filter(
            status='PENDING',
            available_seats__gte=data['seats_needed']
        ).annotate(
            distance_to_pickup=Distance('start_point', data['pickup_point']),
            distance_to_destination=Distance('end_point', data['destination_point'])
        ).filter(
            distance_to_pickup__lte=D(m=data['radius']),
            distance_to_destination__lte=D(m=data['radius'])
        ).order_by('start_time')

    

class RideActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['accept', 'reject'])
    
    def perform_action(self, ride_request, user):
        if user != ride_request.ride.driver:
            raise serializers.ValidationError("You are not authorized to manage this request")
            
        action = self.validated_data['action']
        ride = ride_request.ride
        
        if action == 'accept':
            if ride_request.seats_needed > ride.available_seats:
                raise serializers.ValidationError(f"Only {ride.available_seats} seats available")
                
            ride_request.status = 'CONFIRMED'
            ride.available_seats -= ride_request.seats_needed
        else:
            ride_request.status = 'REJECTED'
            
        ride_request.save()
        ride.save()
        
        return {
            'message': f"Request {action}ed successfully",
            'available_seats': ride.available_seats
        }

class RideStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['ONGOING', 'COMPLETED', 'CANCELLED'])
    
    def update_status(self, ride):
        new_status = self.validated_data['status']
        ride.status = new_status
        ride.save()
        
        if new_status in ['COMPLETED', 'CANCELLED']:
            ride.requests.filter(status='CONFIRMED').update(status=new_status)
            
        return {'message': f"Ride status updated to {new_status}"}

class PassengerStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['IN_VEHICLE'])
    
    def update_status(self, ride_request):
        ride_request.status = self.validated_data['status']
        ride_request.save()
        return {'message': "Status updated to IN_VEHICLE"}
    



from rest_framework import serializers

class EmissionsSavingsSerializer(serializers.Serializer):
    ride_id = serializers.IntegerField()
    distance = serializers.FloatField()
    total_participants = serializers.IntegerField()
    carbon_savings = serializers.FloatField()
