from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
def home(request):
    title='Hello world'
    return render(request,'home.html')

def signup(request):
    if request.method=='GET':
         return render(request,'signup.html',{
        'form':UserCreationForm})
    else:
        pass1=request.POST['password1']
        pass2=request.POST['password2']
        if len(pass1)>=8:           
            if pass1==pass2:
                try:
                    user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                    user.save()
                    login(request,user)
                    return redirect('tasks') 
                   
                except IntegrityError:
                    return render(request,'signup.html',{
            'form':UserCreationForm,
            "error":"El usuario ya existe"    
        })                  
            return render(request,'signup.html',{
            'form':UserCreationForm,
            "error":"La contraseña no coincide"})
            
        else:
             return render(request,'signup.html',{
            'form':UserCreationForm,
             "error":"La contraseña tiene que tener como mínimo  8 caracteres"
        })    

@login_required
def tasks(request):
    ##tasks=Task.objects.all()
    tasks=Task.objects.filter(user=request.user##,datecompleted__isnull=True
                              ) 
    return render (request,'tasks.html',{'tasks':tasks})         
@login_required    
def create_task(request):
    if request.method=='GET':
        return render(request,'create_task.html',{'form':TaskForm})
    else:
         try:
            form=TaskForm(request.POST)
            new_task= form.save(commit=False)
            new_task.user=request.user
            new_task.datecompleted=timezone.now()
            new_task.save()
            return redirect('tasks')
         except ValueError:
             return render(request,'create_task.html',{
                 'form':TaskForm,
                 'error':'Please provide valida data'
             })
@login_required         
def task_detail(request, task_id):
    
    try:
        task=Task.objects.get(pk=task_id, user=request.user ) # user=request.user eso ser'ia para mostrar solo las tareas de ese usuario
        
        return render(request,
                  "task_detail.html",{"task":task})
        
    except Task.DoesNotExist:
        return render(request,
                  "notFound.html")
@login_required
def complete_task(request,task_id):
   task= get_object_or_404(Task,pk=task_id,user=request.user).order_by('-datecompleted')
   if request.method=='POST':
        task.datecompleted=timezone.now()
        task.save()
        return redirect('tasks')
@login_required
def delete_task(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)        
    if request.method=='POST':
        task.delete()
        return redirect('tasks')
@login_required    
def signout(request):    
    logout(request)
    return redirect('home')

def signin(request):
    if request.method=='GET':
        return render(request,'signin.html',{
                  'form':AuthenticationForm})
    else:
       user= authenticate(request,username=request.POST['username'],password=request.POST['password'])
       if user is None:
           return render(request,'signin.html',{
                  'form':AuthenticationForm,
                  'error':'Username or password is incorrect'}) 
       else:
            login(request,user)
            return redirect('tasks')

