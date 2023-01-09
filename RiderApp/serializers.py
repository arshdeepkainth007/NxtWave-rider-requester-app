from rest_framework import serializers
from RiderApp.models import RiderModel


class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderModel
        fields = ('RideID', 'RiderID', 'FromAddress', 'ToAddress', 'DateTime', 'AvailableAssets', 'TravelMedium')

