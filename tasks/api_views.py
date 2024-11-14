from collections import Counter
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .__init__ import *

@api_view(["GET"])
def hi(request):
    return Response(tasks_stor.csv_read(), status=S200)
@api_view(["POST"])
def add(request):
    data = request.data
    # print(data)
    res = tasks_stor.add(data)
    if  not res[0]:
        return Response({"Error":res[1]}, status=S400)
    tasks_stor.save()
    return Response(data , status=S200)
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
    result = Users.create(**data)
    if not result[0]:
        return Response({"Error":result[1]}, status=S422)
    user_dict = result[1].to_save()
    x = users_stor.add(user_dict)
    y= users_stor.save()
    return Response({"success":user_dict, "x":x, "y":y}, status=S201)


@api_view(["POST"])
def login(request):
    data = request.data or None
    username = data.get("username", None)
    password = data.get("password", None)
    if not data or not username  or not password:
        msg = "No"
        msg += "-request data " if not data else None
        msg += "-username"  if not  data.get("username") else ""
        msg += "-password"  if not  data.get("password") else ""
        msg += "Provided"
        return Response({"Error":msg}, status=S400)

    query = users_stor.get_by("username", username)
    if not query[0]:
        return Response({"Error":query[1]}, status=S400)
    # print(f"\n\n\n\n  REQUEST DICT {request.__dict__.keys()}")
    return Response(query[1], status=S200)
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
def test(request, key=None):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    content_type = request.META.get('CONTENT_TYPE', '')

    # Alternatively, to get all headers as a dictionary
    headers = {key: value for key, value in request.META.items() if key.startswith('HTTP_')}
    x = {
        'auth_header': auth_header, 'content_type': content_type,
        "headers":headers
    }
    if key:
        return Response(x[key], status=S200)

    return Response(x, S200)