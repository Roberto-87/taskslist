from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.utils import timezone

# Create your views here.

def home(request):
    return render (request, 'home.html')

def signup(request):
   if request.method=='GET':
       return render(request, 'signup.html',{
           'form':UserCreationForm
       })
   else:
       if request.POST['password1']== request.POST['password2']:
           try:
              user= User.objects.create_user(username= request.POST['username'], password= request.POST['password1'])
              user.save()
              login(request, user)
              return redirect('tasks')
           except IntegrityError:
              return render(request, 'signup.html',{
                'form':UserCreationForm,
                'error':'user already exists'
                })
       return render(request, 'signup.html',{
                'form':UserCreationForm,
                'error':'passwords does not match'
                })      
@login_required   
def tasks(request):
    tasks= Task.objects.filter(user= request.user, date_completed__isnull= True)
    return render(request, 'tasks.html', {"tasks": tasks})   
 
@login_required          
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method== 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user= authenticate(request, username= request.POST['username'], password= request.POST['password'])
        if user is None:    
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
        })
        else:
            login(request, user)
            return redirect('tasks')    
    
@login_required       
def createtask(request):
    if request.method == "GET":
        return render(request, 'createtask.html', {"form": TaskForm})          
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'createtask.html', {"form": TaskForm, "error": "Error creating task."})
         
@login_required
def task_detail(request, task_id):
   if request.method== 'GET':
        task= get_object_or_404(Task, pk=task_id, user=request.user)
        form= TaskForm(instance= task)
        return render(request, 'task_detail.html', {
            'task': task, 'form':form
        })    
   else:
        try:
                task= get_object_or_404(Task, pk=task_id, user= request.user)
                form= TaskForm(request.POST, instance= task)
                form.save()
                return redirect('tasks')  
        except:
            return render(request, 'task_detail.html', {
            'error': 'Error updating task', 'form':form
            })    
            
@login_required                    
def task_complete(request, task_id):
    task= get_object_or_404(Task, pk=task_id, user= request.user)  
    if request.method== 'POST': 
        task.date_completed= timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def task_delete(request, task_id):
     task= get_object_or_404(Task, pk=task_id, user= request.user)  
     if request.method== 'POST': 
        task.delete()
        return redirect('tasks')
    
@login_required    
def task_ended(request):
    tasks= Task.objects.filter(user= request.user, date_completed__isnull= False)
    return render(request, 'task_ended.html', {"tasks": tasks})     