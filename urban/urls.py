from django.conf.urls import url
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views



urlpatterns = [
    url(r'^$', homepage),
    url(r'^login/$', login_user, name='login'),
    url(r'^redirect_user/$', redirect_user),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'create_user/', CreateUser.as_view()),
    url(r'create_task/', create_task, name='create_task'),
    url(r'^task_info/$', TaskInfo.as_view(), name = 'task'),
    url(r'^task_info/(?P<id>\d+)/', TaskInfo.as_view(),name='task_info'),
    url(r'^cancel_task/(?P<id>\d+)/$', CancelTask.as_view(), name='cancel_task'),
    url(r'^task_state/(?P<id>\d+)/$', TaskStateAPI.as_view(), name='task_state'),
    url(r'^task_decline/(?P<id>\d+)/$', DeclineTask.as_view(), name='decline_task'),
    url(r'^task_complete/(?P<id>\d+)/$', CompleteTask.as_view(), name='complete_task'),
    url(r'^show_pending_task/$', ShowPendingTask.as_view(), name='pending_task'),
    url(r'^accepted_pending_task/(?P<id>\d+)$', AcceptPendingTask.as_view(), name='accepted_task'),
]