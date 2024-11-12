from django.shortcuts import (
    render, HttpResponse, redirect
)
from .forms import *
from api.views import now_date, datetime
from .__init__ import *
from uuid import uuid4
from .models import *
def hi(request):
    tasks = tasks_stor. csv_read()
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
            "username":x.get('username'),
            "priority":int(x.get("priority")[0]),
            "kickoff":x.get("kickoff"),

        }
        task_obj = Tasks(**data)
        task_dict  = task_obj.to_save()
        res = tasks_stor.add(task_dict)
        if res[0]:
            tasks_stor.save()
            return redirect("tasks:Hi")

        # print(f"\n\n\n {x}\n")
        # print(f"\n\n\n {TASKS}\n")

    return HttpResponse(f"{res[1]}")

def delete_task(request, task_id):
    res =  tasks_stor.delete("id", task_id)
    print(f"from kosom  delete route {task_id}")
    return redirect("tasks:Hi")
def register(request):
    return render(request, "user_form.html", {"form":UsersForm()})