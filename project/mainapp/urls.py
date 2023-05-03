from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path

routers=DefaultRouter()
routers.register(r'register', Registerset, basename='registration')
routers.register(r'login', Loginviewset, basename='login')
routers.register(r'logout', Logoutviewset, basename='logout')
routers.register(r'eventslist', ShowUpcomingEventsView, basename='eventlist')
routers.register(r'eventdetails', DeatilEventView, basename='detailevent')
routers.register(r'advertisments', AdvertismentView, basename='advertisments')


urlpatterns=routers.urls
urlpatterns+=[
    path('tickets/', Ticketlist.as_view(), name='ticket_list'),
    path('tickets/booking/', EventBookingView.as_view(), name='eventbooking')
]
