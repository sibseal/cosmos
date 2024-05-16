from django.urls import path, include

from .views import (TaskUpdate, update_criterion, update_item, execute, add_item, add_criterion, )
from .views import tasks, add_task, set_task_name, get_answer, add_criteria, add_items, create_task, update_task_v2, login_view, logout_view,delete_task,test
app_name = 'products'  # 3rd

urlpatterns = [
    path('', tasks, name='list_tasks'),
    path('tasks/', tasks, name='list_tasks'),

    path('login/', login_view, name='login_view'),

    path('add_task/', add_task, name='add_task'),
    path('set_task_name/', set_task_name, name='set_task_name'),
    path('get_answer/<str:task_name>/<int:question_id>/', get_answer, name='get_answer'),
    path('create_task/<str:task_name>', create_task, name='create_task'),
    path('add_criteria/<int:task_id>', add_criteria, name='add_criteria'),
    path('add_items/<int:task_id>', add_items, name='add_items'),

    path('task/<int:pk>/', TaskUpdate.as_view(), name='task'),
    path('update_task_v2/<int:task_id>', update_task_v2, name='update_task_v2'),

    path('update-criterion/<int:pk>/', update_criterion, name='update_criterion'),
    path('update-item/<int:pk>/', update_item, name='update_item'),
    path('add-item/<int:task_id>/', add_item, name='add_item'),
    path('add-criterion/<int:task_id>/', add_criterion, name='add_criterion'),

    path('execute/<int:pk>/', execute, name='execute'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),

    path('logout/', logout_view, name='logout_view'),
    path('test/', test, name='test'),
]
