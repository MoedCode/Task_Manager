#ProMarket/web/views.py
from django.shortcuts import render, redirect, HttpResponse

def hi(request):
    return render(request, "Hi.html")