from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .forms import *
from datetime import datetime
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout
from .decorator import check_login_store


class CreateUser(APIView):
    '''
    Creating user through api hit , have a custom flag  is_store_manager for checking user type
    '''

    def post(self,request):
        data = request.data
        email = data["email"]
        password = data["password"]
        username = data["username"]
        is_store_manager = data["is_store_manager"]
        u = User.objects.create_user(email=email, password=password, username=username)
        if is_store_manager:
            user = StoreManager.objects.create(user=u)
        else:
            user = DeliveryPerson.objects.create(user=u)
        return Response({"results" : "User created"}, status=status.HTTP_200_OK)


class TaskInfo(APIView):

    def get_list(self,request):
        qs = Task.objects.all()
        serializer = TaskInfoSerializer(qs, many=True)
        return render(request, 'task_info.html', {'data': serializer.data})

    def get(self, request, id=None):
        if not id:
            self.get_list(request)
        task = Task.objects.get(id=id)
        return render(request, 'task_object_info.html' ,{'elem':task})


class CancelTask(APIView):

    def get(self, request, id=None):
        if id == None:
            return HttpResponse("Bad Request")
        else:
            qs = Task.objects.filter(id=id)
            if qs[0].last_state == Task.State.NEW:
                Task.objects.filter(id=id).update(last_state=Task.State.CANCELLED)
                qs = Task.objects.all()
                serializer = TaskInfoSerializer(qs, many=True)
                return render(request, 'store_manager_homepage.html', {'task_data': serializer.data})
            else:
                return HttpResponse("Can't Cancel an ongoing Task.")

class DeclineTask(APIView):
    def get(self,request,id=None):
        if id == None:
            return HttpResponse("Bad Request")
        else:
            # TaskState.objects.filter(task__id=id).delete()
            task = Task.objects.filter(id=id).update(last_state=Task.State.NEW)
            task.delivered_by = None
            task.save()
            return HttpResponse("Declined Task")

class CompleteTask(APIView):
    def get(self,request,id=None):
        if id == None:
            return HttpResponse("Bad Request")
        else:
            Task.objects.filter(id=id).update(last_state=Task.State.COMPLETED)
            task =Task.objects.filter(id=id)[0]
            TaskState.objects.create(state=TaskState.State.COMPLETED, created=datetime.now(), task=task)
            return HttpResponse("Task Completed")


class TaskStateAPI(APIView):
    def get(self, request, id=None):
        if id == None:
            return HttpResponse("Bad Request")
        else:
            qs = TaskState.objects.filter(task__id=id).order_by('created')
            print(qs,"\n\n\n")
            task_state = TaskStateSerializer(qs,many=True)
            return render(request, 'task_state.html', {'task_state': task_state.data})


class ShowPendingTask(APIView):
    '''
    For showing pending task in queues
    '''
    def get(self, request):
        data = {}
        for elem in Task.objects.filter(last_state='new'):
            temp = {}
            temp["title"]= elem.title
            temp["priority"]= elem.priority
            temp["last_state"]= elem.last_state
            data[elem.id] = temp
        return Response({'results': data})


def show_pending_task():
    '''
    Function for showing pending tasks in queue
    '''
    data = Task.objects.filter(last_state='new').first()
    return data
    data = {}
    for elem in Task.objects.filter(last_state='new'):
        temp = {}
        temp["title"] = elem.title
        temp["priority"] = elem.priority
        temp["last_state"] = elem.last_state
        data[elem.id] = temp
    return data

@check_login_store
def create_task(request):
    '''
    To do : change created_by
    change response
    '''
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            store_manager = StoreManager.objects.get(user=request.user)
            data.created_by = store_manager
            data.created = datetime.now()
            data.save()
            TaskState.objects.create(task=data, created =datetime.now(), state=TaskState.State.NEW)
        return redirect(redirect_user)
    else:
        form = TaskForm()
        return render(request, 'create_task.html', {'form': form})


def homepage(request):
    no_of_store_manager = StoreManager.objects.all().count()
    no_of_delivery_person = DeliveryPerson.objects.all().count()
    return render(request, 'homepage.html',{'store_manager' : no_of_store_manager, 'delivery_person' : no_of_delivery_person})


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            users = authenticate(request, username=username, password=password)
            if users is not None:
                print(users,"\n\n")
                login(request, users)
                return redirect(redirect_user)
        return HttpResponse('User is Not Logged in')
    else:
        form = LoginForm()
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return render(request,'logout.html')


def redirect_user(request):
    delivery = DeliveryPerson.objects.filter(user=request.user)
    store_manager = StoreManager.objects.filter(user=request.user)

    if delivery.count()>0:
        qs = Task.objects.filter(last_state=TaskState.State.ACCEPTED, delivered_by=delivery[0])
        task_data = TaskInfoSerializer(qs,many=True)
        data = show_pending_task()
        pending_data = TaskInfoSerializer(data)
        print(task_data.data)
        return render(request, 'delivery_homepage.html', {'task_data': task_data.data, 'pending_data' :pending_data.data})
    else:
        if store_manager.count()>0:
            qs = Task.objects.filter(created_by=store_manager[0])
            serializer = TaskInfoSerializer(qs, many=True)
            print(serializer.data)
            return render(request, 'store_manager_homepage.html', {'task_data': serializer.data})
        else:
            return HttpResponse("There are no Store Managers")


class AcceptPendingTask(APIView):
    def get(self,request,id=None):
        task =  Task.objects.filter(id=id).update(last_state=Task.State.ACCEPTED)
        task = Task.objects.filter(id=id)
        TaskState.objects.create(state=TaskState.State.ACCEPTED,created=datetime.now(),task=task[0])
        return HttpResponse("Task Accepted")
