from rest_framework import serializers
from .models import*
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class Registerserializer(serializers.ModelSerializer):
    queryset=User.objects.all()
    email=serializers.EmailField(required=True, validators=[UniqueValidator(queryset=queryset)])
    username=serializers.CharField(required=True, validators=[UniqueValidator(queryset=queryset)])
    password=serializers.CharField(required=True,write_only=True, validators=[validate_password])

    class Meta:
        model=User
        fields=['email', 'username', 'password']

        def validate(self, attrs):
            password2=self.context.get('password2')
            if attrs['password2'] != password2:
                raise serializers.ValidationError({'password':'password does not match'})
            return attrs
        
class AdvertismentSerializers(serializers.ModelSerializer):
    class Meta:
        model=Advertisment
        fields='__all__'

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['eventName', 'shortDisc', 'eventImage', 'eventVenue', 'eventDate', 'eventOrganizer', 'basePrice']

class EventsDeatilSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['eventName', 'longDisc', 'eventImage', 'eventVenue', 'eventDate', 'eventOrganizer', 'basePrice']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model=seatCategory
        fields='__all__'

class TicketBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticektbooking
        fields='__all__'



        