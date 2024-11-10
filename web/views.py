#ProMarket/web/views.py
from django.shortcuts import render, redirect, HttpResponse
from api.views import now_date, datetime
def hi(request):
    return render(request, "Hi.html", {"now":now_date()})
def isNY(request):
    now = datetime.now()
    return render(request, "isNY.html",{"isNY":now.month == 1 and now.day == 1 })