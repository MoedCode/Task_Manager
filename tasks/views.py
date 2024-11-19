from django.shortcuts import (
    render, HttpResponse, redirect
)
from .forms import *
from api.views import now_date, datetime
from .__init__ import *
from uuid import uuid4
from .models import *
from .authentication import Authentication
auth = Authentication()

import json
from django.http import JsonResponse

def dump_request_to_json(request, filename="request_dump.json"):
    try:
        # Extract relevant parts of the request
        request_data = {
            "method": request.method,
            "headers": dict(request.headers),  # Convert headers to a dictionary
            "GET_params": dict(request.GET),  # Query parameters
            "POST_data": request.POST.dict(),  # Form data
            "body": request.body.decode("utf-8"),  # Raw body, decoded
            "content_type": request.content_type,
            "path": request.path,
            "cookies": request.COOKIES,
            "session": dict(request.session.items()) if request.session else None,

        }

        # Write to a JSON file
        with open(filename, "w") as file:
            json.dump(request_data, file, indent=4)

        print(f"Request data has been dumped to {filename}")
        return JsonResponse({"status": "success", "message": f"Request data dumped to {filename}"})
    except Exception as e:
        print(f"Error dumping request data: {e}")
        return JsonResponse({"status": "error", "message": str(e)})

def hi(request):
    dump_request_to_json(request)
    msg = ""
    print(f"\n\n from view:hi  token 1 {request.headers.get('Authorization')} \n")

    tasks = tasks_stor.csv_read()
    token_x = request.COOKIES.get("auth_token")
    query_token  = tokens_stor.get_by(key="token", value=token_x)
    print(f"\n\n from view:hi  token {token_x} \n")

    msg = query_token[1]
    return render(request, "Hi.html", {
        "now": now_date(),
        "tasks": tasks,
        "app_token": query_token,
        "req_token":token_x

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
    return render(request, "register.html", {"form":UsersForm()})

def  login( request):
    return render(request, "login.html")