from django.shortcuts import render
from rest_framework import viewsets, generics
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from .models import *
from django.contrib.auth import logout
from rest_framework import status
import datetime

# Create your views here.

class Registerset(viewsets.ViewSet):
    queryset=User.objects.all()
    permission_classes=[AllowAny]
    def create(self, request):
        data=request.data
        password=data['password']
        serializer_class=Registerserializer(data=data, context={'password2':data['password2']})
        serializer_class .is_valid(raise_exception=True)
        user=serializer_class.save()
        user.set_password(user.password)
        user.save()
        token=Token.objects.create(user=user)
        return Response({'data':serializer_class.data, 'Token':token.key}, status=status.HTTP_201_CREATED)

class Loginviewset(viewsets.ViewSet):
    queryset=User.objects.all()
    def create(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            return Response("User with this username does not exit")
        if not check_password(password, user.password):
            return Response("Password incorrect")
        Token.objects.get(user=user).delete()
        token=Token.objects.create(user=user)
        return Response({'Token': str(token)}, status=status.HTTP_202_ACCEPTED)
    
class Logoutviewset(viewsets.ViewSet):
    queryset=User.objects.all()
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def list(self,request):
        request.user.auth_token.delete()
        logout(request)
        msg={'Sucess': 'You are logged out'}
        return Response(data=msg, status=status.HTTP_200_OK)
class AdvertismentView(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Advertisment.objects.all()
    serializer_class=AdvertismentSerializers
    http_method_names=['get']
    
class ShowUpcomingEventsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    http_method_names = ['get']

class DeatilEventView(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Event.objects.all()
    serializer_class=EventsDeatilSerializer
    http_method_names=['get']

class Ticketlist(generics.ListCreateAPIView):
    queryset=Ticektbooking.objects.all()
    serializer_class=TicketSerializer

class Ticketdetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Ticektbooking.objects.all()
    serializer_class=TicketSerializer

class SeatDetail(APIView):
    def get(self, request, pk, seat_pk):
        ticket = get_object_or_404(Ticektbooking, pk=pk)
        seat = get_object_or_404(Seat, pk=seat_pk, ticket=ticket)
        serializer = SeatSerializer(seat)
        return Response(serializer.data)

    def put(self, request, pk, seat_pk):
        ticket = get_object_or_404(Ticektbooking, pk=pk)
        seat = get_object_or_404(Seat, pk=seat_pk, ticket=ticket)
        serializer = SeatSerializer(seat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

