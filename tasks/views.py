from django.shortcuts import render, HttpResponse
from .forms import TaskForm
from api.views import now_date, datetime
def hi(request):
    return render(request, "Hi.html", {"now":now_date()})

def add(request):
    if request.method == "GET":
        return render(request, "add.html", {"form":TaskForm()})
    if request.method == "POST":
        print("\n\n\n Post data \n\n\n",request.POST)
    return HttpResponse("something went wrong ")

