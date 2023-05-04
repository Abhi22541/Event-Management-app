from django.shortcuts import render
from rest_framework import viewsets, generics
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
from django.contrib.auth.models import User

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
    serializer_class=TicketBookingSerializer

# class Ticketdetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Ticektbooking.objects.all()
#     serializer_class=TicketSerializer
# class TicketBookview(APIView):
#     def post(self, request, format=None):
#         data=request.data
#         print(data)
#         bookingSeats=data['seatquantity']
#         bookedSeats=bookingSeats
#         if Seat.avaiblity<bookedSeats:
#             return Response("Total seats is "+str(Seat.avaiblity)+", so please choose seat in the limit")
#         remSeats=Seat.avaiblity-bookedSeats
#         Seat.avaiblity=remSeats
#         Seat.save()
#         seatsAmount=bookedSeats*Seat.price

#         serializers=TicketBookingSerializer
#         serializers.is_valid(raise_exception=True)
#         Ticektbooking=serializers.save()

#         return Response({'info':'your'+str(bookedSeats)+'seats Ticket Booked and ticket number is: ', data:serializers.data})

class EventBookingView(APIView):
    # permission_classes=[IsAuthenticated]
    def post(self, request):
        userid=request.data.get('user')
        bookingID=request.data.get('id')
        eventName=request.data.get('event name')
        categoryName=request.data.get('seat')
        quantity=request.data.get('quantity')
        bookedseat=int(quantity)
        


        # try:
        #     user=Attendee.objects.get(pk=userid)
        # except:
        #     return Response("invalid user")
        
        # if request.user!=user:
        #     return Response("you have not permisson to do that")
        
        try:
            category=seatCategory.objects.get(id=categoryName)
            if bookedseat>category.seatAvailable:
                return Response({'error':'not enough seats available'})
        except seatCategory.DoesNotExist:
            return Response({'error':'Invalid Category'})
        
        try:
            event = Event.objects.get(eventName=eventName)
        except Event.DoesNotExist:
            return Response({'error': 'Invalid event'})
        
        price=category.price
        totalPrice=bookedseat*price

        booking= Ticektbooking(
            bookingID=bookingID,
            event=event,
            seatquantity=bookedseat,
            totalprice=price,
            
        )
        
        booking.save()
        booking.seat.set(categoryName)
        booking.save()
        category.seatAvailable-=bookedseat
        category.save()

        try:
            userBal=Attendee.objects.get(user=userid)
        except:
            return Response("please register yourself")
        
        requiredamount=totalPrice-userBal.balance
        if totalPrice>userBal.balance:
            return Response("Low balance please add amount"+ "please add rmainig amount to your account "+ str(requiredamount))
        updatedBalance=userBal.balance-totalPrice
        userBal.balance=updatedBalance
        userBal.save()
        # serializer=TicketBookingSerializer
        # serializer.is_valid(raise_exception=True)
        # ticket=serializer.save()

        


        return Response({
            'bookingID':booking.bookingID, 
            'priceperseat':price ,
            'totalprice':totalPrice, 
            'availableseats':category.seatAvailable, 
            'seatbook':category.categoryName, 
            'seat quantity':bookedseat,
            'remainig balance':userBal.balance
            })

        



