from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Advertisment(models.Model):
    comapnyName=models.CharField(max_length=60, null=True)
    advImage=models.FileField(upload_to='addImage')
    def __str__(self):
        return self.comapnyName

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
    balance=models.PositiveIntegerField(null=True)
    
    
    def __str__(self):
        return self.user.username
    
    
# class Ticket(models.Model):
#     SEAT=(('VVIP', 'FIRST CLASS'),
#           ('VIP', 'SECOND CLASS'),
#           ('NORMAL', 'THIRD CLASS'))
    

    
class seatCategory(models.Model):
    event=models.ManyToManyField(Event)
    categoryName=models.CharField(max_length=20)
    price=models.IntegerField()
    seatAvailable=models.IntegerField()
    active=models.BooleanField()

    def __str__(self):
        return self.categoryName+'.'+str(self.id)
    
class Ticektbooking(models.Model):
    bookingID=models.CharField(max_length=20)
    attende=models.ForeignKey(Attendee, on_delete=models.CASCADE, null=True, blank=True)
    event=models.ForeignKey(Event, on_delete=models.CASCADE)
    seat=models.ManyToManyField(seatCategory)
    seatquantity=models.IntegerField()
    totalprice=models.IntegerField()
    bookingDate=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bookingID+'-'+self.attende.user.username+'-'+self.event.eventName
    class Meta:
        ordering=['totalprice']






