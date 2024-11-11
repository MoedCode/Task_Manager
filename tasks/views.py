from django.shortcuts import (
    render, HttpResponse, redirect
)
from .forms import TaskForm
from api.views import now_date, datetime
from .__init__ import *
from uuid import uuid4
def hi(request):
    tasks = csv_stor. csv_read()
    return render(request, "Hi.html", {
        "now":now_date(), "tasks":tasks
        })

def add(request):
    if request.method == "GET":
        return render(request, "add.html", {"form":TaskForm()})
    if request.method == "POST":
        x  = request.POST
        data =  {
            "task":x.get('task'),
            "priority":int(x.get("priority")[0]),
            "kickoff":x.get("kickoff"),
            "id":str(uuid4())
        }
        res = csv_stor.add(data)
        if res[0]:
            csv_stor.save()
            return redirect("tasks:Hi")

        # print(f"\n\n\n {x}\n")
        # print(f"\n\n\n {TASKS}\n")

    return HttpResponse(f"{res[1]}")

def delete_task(request, task_id):
    return HttpResponse("<h1>lef we arg3 tany</h1>")
