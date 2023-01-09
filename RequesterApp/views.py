from django.shortcuts import render

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status as http_satus
from rest_framework.response import Response
from rest_framework.decorators import api_view

from NxtwaveAPI.pagination import StandardResultsSetPagination
from RequesterApp.models import RequesterModel
from RequesterApp.serializers import RequesterSerializer
from RiderApp.models import RiderModel
from RiderApp.serializers import RiderSerializer





@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def RequestAPI(request,request_id=None):
    # This is to for one request
    response = {
        "data": None,
        "message": None
    }
    if request.method == 'GET':
        paginator = StandardResultsSetPagination()
        
        if not request_id:
            requests_doc = RequesterModel.objects.all()
            result_page = paginator.paginate_queryset(requests_doc, request)
            request_serializer = RequesterSerializer(result_page, many=True)
            return paginator.get_paginated_response(request_serializer.data)
        else:
            request_doc = RequesterModel.objects.get(RequestID=request_id)
            request_serializer = RequesterSerializer(request_doc)
            response["data"] = request_serializer.data,
            response["message"] = "GET call successfull"
            return Response(response, status=http_satus.HTTP_202_ACCEPTED) 

    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        request_serializer = RequesterSerializer(data = request_data)
        if request_serializer.is_valid(raise_exception=True):
            request_serializer.save()
            response["data"] = request_serializer.data
            response["message"] = "Added Successfully"
            return Response(response, status=http_satus.HTTP_202_ACCEPTED)
        response["message"] = "Failed to add"
        return Response(response, status=http_satus.HTTP_406_NOT_ACCEPTABLE)

    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        request_doc = RequesterModel.objects.get(RequestID=request_id)
        request_serializer = RequesterSerializer(request_doc,data=request_data)
        if request_serializer.is_valid(raise_exception=True):
            request_serializer.save()
            response["data"] = request_serializer.data,
            response["message"] = "Update Successfully"
            return Response(response, status=http_satus.HTTP_202_ACCEPTED)
        response["message"] = "Failed to update"
        return Response(response, status=http_satus.HTTP_406_NOT_ACCEPTABLE)

    elif request.method == 'DELETE':
        if not request_id:
            response["message"] = "Please provide request id"
            return Response(response, status=http_satus.HTTP_406_NOT_ACCEPTABLE)
        request = request = RequesterModel.objects.get(RequestID=request_id)
        request.delete()
        response["message"] = "Deleted request successfully"
        return Response(response, status=http_satus.HTTP_202_ACCEPTED)


@csrf_exempt
@api_view(['GET'])
def RequesterAPI(request):
    response = {
        "data": None,
        "message": None
    }
    if request.method == 'GET':
        if not request.GET['requester_id']:
            response["message"] = "Please provide requester id"
            return Response(response, status=http_satus.HTTP_406_NOT_ACCEPTABLE)
        paginator = StandardResultsSetPagination()

        status = request.GET.get('status', None)
        asset_type = request.GET.get('asset_type', None)
        ordering = request.GET.get('ordering', "false")
        requests = RequesterModel.objects.filter(RequesterID=request.GET['requester_id'])
        if status:
            requests = requests.filter(Status=status)
        if asset_type:
            requests = requests.filter(AssetType=asset_type)
        if ordering == "true":
            requests = requests.order_by("DateTime")
        
        result_page = paginator.paginate_queryset(requests, request)
        request_serializer = RequesterSerializer(result_page, many=True)
        return paginator.get_paginated_response(request_serializer.data)


@csrf_exempt
@api_view(['GET', 'POST'])
def MatchingRidesAPI(request, request_id=None):
    response = {
        "data": None,
        "message": None
    }
    if request.method == 'GET':
        if not request_id:
            response["message"] = "Please provide request id for rides to match with"
            return Response(response, status=http_satus.HTTP_406_NOT_ACCEPTABLE)
        request_doc = RequesterModel.objects.get(RequestID=request_id)
        request_serializer = RequesterSerializer(request_doc)
        from_address = request_serializer.data.get("FromAddress")
        to_address = request_serializer.data.get("ToAddress")
        date = request_serializer.data.get("DateTime")
        number_of_assets = request_serializer.data.get("NumberOfAssets")
        status = request_serializer.data.get("Status")
        if status != "-":
            response["message"] = "The provided request id is either matched or completed"
            return Response(response, status=http_satus.HTTP_422_UNPROCESSABLE_ENTITY)
        
        paginator = StandardResultsSetPagination()

        rides = RiderModel.objects.filter(FromAddress=from_address, ToAddress=to_address, DateTime=date, Status = "-", AvailableAssets__gte = number_of_assets)
        result_page = paginator.paginate_queryset(rides, request)
        ride_serializer = RiderSerializer(result_page, many=True)
        return paginator.get_paginated_response(ride_serializer.data)
        
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        request_id = request_data.get("request_id")
        ride_id = request_data.get("ride_id")
        if not request_id or not ride_id:
            response["message"] = "Please provide both request_id and ride_id"
            return Response(response, status=http_satus.HTTP_406_NOT_ACCEPTABLE)

        request_doc = RequesterModel.objects.get(RequestID=request_id)
        ride_doc = RiderModel.objects.get(RideID=ride_id)
        request_serializer = RequesterSerializer(request_doc)
        ride_serializer = RiderSerializer(ride_doc)
        if ride_serializer.data.get("RequestID") or request_serializer.data.get("RideID"):
            response["message"] = "Either ride or request status is already confirmed"
            return Response(response, status=http_satus.HTTP_422_UNPROCESSABLE_ENTITY)
        request_doc.RideID = ride_id
        request_doc.Status = 'O'
        request_serializer = RequesterSerializer(request_doc)
        request_serializer = RequesterSerializer(request_doc,data=request_serializer.data)

        ride_doc.RequestID = request_id
        ride_doc.Status = 'O'
        ride_serializer = RiderSerializer(ride_doc)
        ride_serializer = RiderSerializer(ride_doc, data=ride_serializer.data)

        if request_serializer.is_valid(raise_exception=True) and ride_serializer.is_valid(raise_exception=True):
            request_serializer.save(update_fields=['RideID','Status'])
            ride_serializer.save(update_fields=['RequestID', 'Status'])
            response["data"] = request_serializer.data,
            response["message"] = "Matched Successfully"
            return Response(response, status=http_satus.HTTP_202_ACCEPTED)
        response["message"] = "Could not update, validation failed"
        return Response(response, status=http_satus.HTTP_422_UNPROCESSABLE_ENTITY)