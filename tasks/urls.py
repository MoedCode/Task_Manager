from django.urls import path
from . import views
from . import api_views
app_name = "tasks"
urlpatterns = [
    path('', views.hi, name="Hi"),
    path('api', api_views.hi, name="HiAPI"),
    path('add', views.add, name="index"),
    path('api/add', api_views.add, name="addAPI"),
    path('post', views.add, name="post_task"),
    path('delete/<str:task_id>', views.delete_task, name="delete"),
    path('api/selection/', api_views.selection_list, name="selection")

]