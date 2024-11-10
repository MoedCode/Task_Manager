from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .__init__ import *

from datetime import datetime

def now_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@api_view(['GET'])
def hi(request):
    return Response({"success":True,"message":"Hello", "visit time":now()}, status=S200)