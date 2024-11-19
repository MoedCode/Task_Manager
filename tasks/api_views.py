from collections import Counter
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .__init__ import *
from .authentication import Authentication

auth = Authentication()
token4test = "NULL"
@api_view(["GET"])
def hi(request):
    return Response(tasks_stor.csv_read(), status=S200)
@api_view(["POST"])
def add(request):
    data = request.data or None
    if not data:
        return Response({"status":"Error", "message":"No Data provided"}, S400)
    task_data =  {
        "task":data.get('task'),
        "username":data.get('username'),
        "priority":int(data.get("priority")[0]),
        "kickoff":data.get("kickoff"),

    }
    task_obj = Tasks(**task_data)
    task_dict  = task_obj.to_save()
    res = tasks_stor.add(task_dict)
    if  not res[0]:
        return Response({"Error":res[1]}, status=S400)
    tasks_stor.save()
    return Response(res[1] , status=S200)
@api_view(["POST"])
def selection_list(request):
    data =  request.data or {}
    select_by = data.get("select_by" , None)
    select_in = data.get("select_in" , None)
    val_lst   = data.get("val_lst", None)


    if not data or not select_by or not val_lst or not select_in:
        msg = "No "
        msg += "Request Data, " if not data else ""
        msg += "selection key," if not select_by else ""
        msg += "selection area," if not select_in else ""
        msg += "selection Values," if not val_lst else ""
        msg += "provided ."
        return Response({"Error":msg}, status=S400)
    if select_in not in Storages_keys:
        return  Response({"Error":f"{select_in} invalid value"}, status=S400)
    stor_type = Storages[select_in]
    quay = stor_type.multi_selection(select_by=select_by, val_lst=val_lst)
    if not quay[0]:
        return Response({"Error":quay[1]}, status=S400)
    return Response(quay[1], status=S200)


@api_view(["POST"])
def register(request):
    data = request.data or {}

    if not data or not len(data.keys()):
        return Response({"Error":"No Valid Data"}, status=S400)
    # not_match = []
    # for key in list(data.keys()):
    #     if key not in Users.KEYS:
    #         not_match.append(key)
    not_match = [key for key in data.keys() if key not in Users.KEYS]
    if len(not_match):
        msg = f"key provided {not_match} not match {Users.KEYS}"
        return Response({"Error":msg}, status=S400)
    username = data["username"]
    email = data["email"]
    username_query = users_stor.is_exist("username", data["username"])
    email_query = users_stor.is_exist("email", data["email"])
    if username_query[0] == "Exist":
        return Response({"status":"error", "message": f"user with username {username} is exist"}, status=S400)
    if email_query[0] == "Exist":
        return Response({"status":"error", "message": f"user with email {email} is exist"}, status=S400)

    result = Users.create(**data)
    if not result[0]:
        return Response({"Error":result[1]}, status=S422)
    user_dict = result[1].to_save()
    x = users_stor.add(user_dict)
    y= users_stor.save()
    log_res = auth.login_user(user_dict)
    if not log_res:
        return  Response({"Error":f"{log_res[1]}"}, status=S400)
    token = log_res[1]
    response = Response({f"success {token}":user_dict, "x":x, "y":y}, status=S201)
    response["Authorization"] = f"Bearer {token}"
    print(f"\n\n from api_views:register >> \n token type: {type(token)} ,  token: {token} \n")
    return response


@api_view(["POST"])
def login(request):
    data = request.data or None
    username = data.get("username", None)
    password = data.get("password", None)
    if not data or not username  or not password:
        msg = "No: "
        msg += "-request data, " if not data else None
        msg += "-username, "  if not  data.get("username") else ""
        msg += "-password, "  if not  data.get("password") else ""
        msg += "Provided"
        return Response({"Error":msg}, status=S400)
    res = auth.authenticate(username=username, password=password)
    if not res[0]:
        return Response({"status":"Error", "message":res[1] }, status=S400)
    login_res = auth.login_user(res[1])
    # print(f"\n\n\n\n  REQUEST DICT {request.__dict__.keys()}")
    if not login_res[0]:
        return Response({"status":"error","message":f"{login_res[1]}"}, S400)
    token = login_res[1]
    response = Response({"status":"success", "message":f"its kaky {login_res[1]}"}, status=S200)
    global  token4test
    token4test =  token
    response["Authorization"] = f"Bearer {token}"
    return response

req_tst= {
    "select_by":"id", "val_lst":["5a710515-e933-497d-b666-8922ce0269ce", "5a710515-e933-497d-b666-8922ce0269ce"]
}
user0 = {
    "username": "johziko",
    "email": "john@example.com",
    "password": "securePassword123",
    "image": "profile.jpg"
}

@api_view(["GET"])
def test(request):

    x=  request.headers.get("Authorization")

    return Response({"message":f"{x}"}, status=S200)


message = """Query {
     'class_name': 'Users', 'created': '2024-11-16T15:24:02.483637',
     'email': 'john@example.com', 'id': '08930ec8-284e-4bca-ac80-d089f144948a',
     'image': 'profile.jpg', 'password': \"b'$2b$12$SxeqOOn.qZNOo7DkOJeHJOGbwjEycnI4dph4T0uZdxXOmsXzoobHK'\",
     'updated': '2024-11-16T15:24:02.483646', 'username': 'johziko'} hashpass 4dbd5e49147b5102ee2731ac03dd0db7decc3b8715c3df3c1f3ddc62dcbcf86d

     """