from django.shortcuts import render,redirect
from .models import Task
from .forms import TaskForm, CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

@unauthenticated_user
def loginUser(request):
    if(request.method=='POST'):
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'Username or Password is incorrect')
            # return render(request, 'accounts/login.html',content)
    return render(request,'baseApp/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerUser(request):
    form=CreateUserForm()
    
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            # Task.objects.create(
            #     user=user)
            messages.success(request,'Account was created for ' + username)
            return redirect('login')
    content={'form':form}
    return render(request, 'baseApp/register.html', content)
    

@login_required(login_url='login')
def home(request):
    search=request.GET.get('search-area') or ''
    tasks= Task.objects.filter(user=request.user, title__icontains=search)
    content={'tasks':tasks, 'search_input':search}

    
    return render(request, 'baseApp/home.html', content)

@login_required(login_url='login')
def taskDetail(request,pk):
    task=Task.objects.get(id=pk)
    content={'task':task}
    return render(request,'baseApp/task_detail.html',content)

@login_required(login_url='login')
def createTask(request):
    
    form= TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect('home')
    
    content={'form': form}
    return render(request, 'baseApp/task_form.html', content)

@login_required(login_url='login')
def updateTask(request,pk):
    task=Task.objects.get(id=pk)
    form= TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    content={'form': form}
    return render(request, 'baseApp/task_form.html', content)

@login_required(login_url='login')
def deleteTask(request, pk):
    task=Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    content={'id':task.id}
    return render(request,'baseApp/delete.html', content)


    
