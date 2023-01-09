from RequesterApp.models import RequesterModel
from RequesterApp.serializers import RequesterSerializer

class MatchRides:

    @classmethod
    def get_matching_rides(cls, request_id = None):
        if not request_id:
            return []
        request = RequesterModel.objects.get(RequestID=request_id)
        request_serializer = RequesterSerializer(request)
        return