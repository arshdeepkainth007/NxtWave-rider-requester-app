from rest_framework import serializers
from RequesterApp.models import RequesterModel


class RequesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequesterModel
        fields = ('RequestID', 'RequesterID', 'FromAddress', 'ToAddress', 'DateTime', 'NumberOfAssets', 'AssetType', 'Senstivity', 'Status', 'RideID')
