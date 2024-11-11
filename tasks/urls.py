from django.urls import path
from . import views
app_name = "tasks"
urlpatterns = [
    path('', views.hi, name="Hi"),
    path('add', views.add, name="index"),
    path('post', views.add, name="post_task"),
    path('delete/<str:task_id>', views.delete_task, name="delete")

]