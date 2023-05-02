from django.shortcuts import render,redirect
#from .forms import TaskForm
from django.http import HttpResponseRedirect
from .models import TaskList
from .forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    if request.method == 'POST':
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
        messages.success(request, "Task Added!")
        return redirect('index')
    else:
        all_tasks = TaskList.objects.filter(owner = request.user)
        paginator = Paginator(all_tasks, 4)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        return render (request, 'taskmate/index.html', {'all_tasks' : all_tasks})
    
def delete_task(request, task_id):
    task = TaskList.objects.get(pk = task_id)
    if task.owner == request.user:
        task.delete()
        messages.success(request, "Task Deleted!")
    else: 
        messages.error(request, "Access Restricted, You aren't allowed!") 
    return redirect('index')


def done_task(request, task_id):
    task = TaskList.objects.get(pk = task_id)
    if task.owner == request.user:
        if task.done:
            task.done = False
            messages.success(request, "Status Updated")
            
        else:
            task.done = True
            messages.success(request, "Status Updated")
    
    else:
        messages.error(request, "Access Restricted, You aren't allowed!")
    
    task.save()
    return redirect('index')



def edit_task(request, task_id):
    if request.method == 'POST':
        task = TaskList.objects.get(pk = task_id)
        form = TaskForm(request.POST or None, instance = task)
        if form.is_valid():
            form.save()
        messages.success(request, "Task Edited!")
        return redirect('index')
    else:
        task_obj = TaskList.objects.get(pk = task_id)
        return render (request, 'taskmate/edit.html', {'task_obj' : task_obj})
    

def homepage(request):
    return render(request, 'taskmate/homepage.html')


