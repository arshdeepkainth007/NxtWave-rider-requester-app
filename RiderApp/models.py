from django.db import models

# Create your models here.

TRAVEL_MEDIUM = (
    ('B', 'Bus'),
    ('C', 'Car'),
    ('T', 'Train')
)

STATUS = {
    ('-', 'PENDING'),
    ('X', 'EXPIRED'),
    ('O', 'CONFIRMED')
}

class RiderModel(models.Model):
    RideID = models.AutoField(primary_key=True)
    RiderID = models.IntegerField()
    FromAddress = models.CharField(max_length=500)
    ToAddress = models.CharField(max_length=500)
    DateTime = models.DateField()
    AvailableAssets = models.IntegerField() # TODO: if the rider has availability, he can get request from more than more requester if asset number if less than available
    TravelMedium = models.CharField(max_length=1, choices = TRAVEL_MEDIUM)
    Status = models.CharField(max_length=1, choices=STATUS, default='-')
    RequestID = models.IntegerField(null=True, default=None)
    # TODO: add flexible timings