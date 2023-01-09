from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from NxtwaveAPI.pagination import StandardResultsSetPagination
from RiderApp.models import RiderModel
from RiderApp.serializers import RiderSerializer

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def RideAPI(request,ride_id=None):
    # This is to for one request
    response = {
        "data": None,
        "message": None
    }
    if request.method == 'GET':
        paginator = StandardResultsSetPagination()
        if not ride_id:
            rides = RiderModel.objects.all()
            result_page = paginator.paginate_queryset(rides, request)
            ride_serializer = RiderSerializer(result_page, many=True)
            return paginator.get_paginated_response(ride_serializer.data)
            # return JsonResponse("Please provide ride id", safe=False)
        else:
            ride = RiderModel.objects.get(RideID=ride_id)
            ride_serializer = RiderSerializer(ride)
        response["data"] = ride_serializer.data,
        response["message"] = "GET call successfull"
        return Response(response, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'POST':
        ride_data = JSONParser().parse(request)
        ride_serializer = RiderSerializer(data = ride_data)
        if ride_serializer.is_valid(raise_exception=True):
            ride_serializer.save()
            response["data"] = ride_serializer.data
            response["message"] = "Added Successfully"
            return Response(response, status=status.HTTP_202_ACCEPTED)
        response["message"] = "Failed to add, validation failed"
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

    elif request.method == 'PUT':
        ride_data = JSONParser().parse(request)
        ride = RiderModel.objects.get(RideID=ride_id)
        ride_serializer = RiderSerializer(ride,data=ride_data)
        if ride_serializer.is_valid():
            ride_serializer.save()
            response["data"] = ride_serializer.data,
            response["message"] = "Update Successfully"
            return Response(response, status=status.HTTP_202_ACCEPTED)
        response["message"] = "Failed to update"
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

    elif request.method == 'DELETE':
        print("Call came here")
        if not ride_id:
            response["message"] = "Please provide ride id for deleting"
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
        ride = RiderModel.objects.get(RideID=ride_id)
        ride.delete()
        response["messate"] = "Deleted request successfully"
        return Response(response, status=status.HTTP_202_ACCEPTED)


@csrf_exempt
@api_view(['GET'])
def RiderAPI(request, rider_id=None):
    response = {
        "data": None,
        "message": None
    }
    if request.method == 'GET':
        if not rider_id:
            response["message"] = "Please provide rider id"
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
        paginator = StandardResultsSetPagination()
        rides = RiderModel.objects.filter(RiderID=rider_id)
        result_page = paginator.paginate_queryset(rides, request)
        ride_serializer = RiderSerializer(result_page, many=True)
        return paginator.get_paginated_response(ride_serializer.data)