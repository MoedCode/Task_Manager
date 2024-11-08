from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .__init__ import *

# Create your views here.
@api_view(['GET'])
def hi(request):
    return Response({"success":True,"message":"Hello"}, status=S200)