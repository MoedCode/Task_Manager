from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .__init__ import *
@api_view(["GET"])
def hi(request):
    return Response(csv_stor.csv_read(), status=S200)
@api_view(["POST"])
def add(request):
    data = request.data
    # print(data)
    res = csv_stor.add(data)
    if  not res[0]:
        return Response({"Error":res[1]}, status=S400)
    csv_stor.save()
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
    quay = csv_stor.multi_selection(select_by=select_by, val_lst=val_lst)
    if not quay[0]:
        return Response({"Error":quay[1]}, status=S400)
    return Response(quay[1], status=S200)
req_tst= {
    "select_by":"id", "val_lst":["5a710515-e933-497d-b666-8922ce0269ce", "5a710515-e933-497d-b666-8922ce0269ce"]
}