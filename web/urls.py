from django.urls import path
from . import views
urlpatterns = [
    path('isnewyear', views.isNY, name="index")
]