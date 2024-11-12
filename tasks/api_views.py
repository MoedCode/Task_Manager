from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .__init__ import *
@api_view(["GET"])
def hi(request):
    return Response(csv_stor.csv_read(), status=S200)
@api_view(["POST"])
def add(request):
    data = request.data
    # print(data)
    res = csv_stor.add(data)
    if  not res[0]:
        return Response({"Error":res[1]}, status=S400)
    csv_stor.save()
    return Response(data , status=S200)