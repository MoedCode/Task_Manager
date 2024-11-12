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
    data =  request.data or None
    select_by = data.get("select_by" , None)
    val_lst   = data.get("val_lst", None)


    if not data or not select_by or not val_lst:
        msg = "No Valid Request Data"
        msg += "invalid selection key" if not select_by else ""
        msg += "invalid selection Values" if not val_lst else ""
        return Response({"Error":msg}, status=S400)
    quay = tasks_stor.multi_selection(select_by=select_by, val_lst=val_lst)
    if not quay[0]:
        return Response({"Error":quay[1]}, status=S400)
    return Response(quay[1], status=S200)
req_tst= {
    "select_by":"id", "val_lst":["5a710515-e933-497d-b666-8922ce0269ce", "5a710515-e933-497d-b666-8922ce0269ce"]
}
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
    if not[0]:
        return Response({"Error":result[1]}, status=S422)
    user_dict = result[1].to_save()
    x = users_stor.add(user_dict)
    users_stor.save()
    return Response({"success":user_dict, "x":x}, status=S201)