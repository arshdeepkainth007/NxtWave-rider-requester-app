from django.db import models

ASSET_TYPES = (
    ('L','LAPTOP'),
    ('T', 'TRAVEL_BAG'),
    ('P', 'PACKAGE')
)

ASSET_SENSTIVITY = (
    ('H', 'HIGHLY_SENSITIVE'),
    ('S', 'SENSITIVE'),
    ('N', 'NORMAL')
)

STATUS = {
    ('-', 'PENDING'),
    ('X', 'EXPIRED'),
    ('O', 'CONFIRMED')
}

class RequesterModel(models.Model):
    RequestID = models.AutoField(primary_key=True)
    RequesterID = models.IntegerField()
    FromAddress = models.CharField(max_length=500)
    ToAddress = models.CharField(max_length=500)
    DateTime = models.DateField()
    NumberOfAssets = models.IntegerField()
    AssetType = models.CharField(max_length=1, choices=ASSET_TYPES, default='P')
    Senstivity = models.CharField(max_length=1, choices=ASSET_SENSTIVITY, default='N')
    Status = models.CharField(max_length=1, choices=STATUS, default='-')
    RideID = models.IntegerField(null=True, default=None)
    # TODO: add flexible timings
