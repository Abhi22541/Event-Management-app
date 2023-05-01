from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Advertisment(models.Model):
    advImage=models.FileField(upload_to='addImage')

class Event(models.Model):
    eventName=models.CharField(max_length=100)
    shortDisc=models.TextField(max_length=200)
    longDisc=models.TextField(max_length=500)
    eventVenue=models.CharField(max_length=150)
    eventDate=models.DateTimeField(auto_now_add=True)
    eventImage=models.ImageField(upload_to='eImage')
    basePrice=models.PositiveIntegerField(null=True)
    eventOrganizer=models.CharField(max_length=100)

    def __str__(self):
        return self.eventName

class Attendee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    contactNumber = models.CharField(max_length=20, null=True)
    eventAttending = models.ManyToManyField(Event, related_name='attendees')
    
    def __str__(self):
        return self.user.username
    
class Seat(models.Model):
    SEAT=(('VVIP', 'FIRST CLASS'),
          ('VIP', 'SECOND CLASS'),
          ('NORMAL', 'THIRD CLASS'))
    seatType=models.CharField(max_length=20, choices=SEAT)

    def __Str__(self):
        return str(self.seatType)

class Seatsavailable(models.Model):
    seatCategory=models.OneToOneField(Seat, on_delete= models.CASCADE)
    avaiblity=models.IntegerField()
    event=models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.avaiblity)


class Ticektbooking(models.Model):
    bookingID=models.CharField(max_length=20)
    attende=models.ForeignKey(Attendee, on_delete=models.CASCADE)
    event=models.ForeignKey(Event, on_delete=models.CASCADE)
    seat=models.ForeignKey(Seat, on_delete=models.CASCADE)
    seatavailable=models.ForeignKey(Seatsavailable, on_delete=models.CASCADE)
    seatquantity=models.IntegerField()
    price=models.IntegerField()
    bookingDate=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bookingID+'-'+str(self.bookingDate)





