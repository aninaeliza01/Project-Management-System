from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
import json

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)

                if user.is_builder:
                    request.session["username"] = user.username
                    return redirect(reverse('user_dashboard')) 
                elif user.is_superuser:
                    request.session["username"] = user.username
                    return redirect(reverse('admin_dashboard')) 
              
            else:
               
                
                return redirect(reverse('login'))
        else:
           
            messages.error(request, "Please provide both username and password.")
            return redirect(reverse('login'))
    
    
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})



@never_cache
@login_required(login_url='login')
def admin_dashboard(request):
    builders = Builder.objects.all()
    return render(request, 'admin_dashboard.html', {'builders': builders})

@never_cache
@login_required(login_url='login')
def user_dashboard(request):
    
    try:
        
        projects = Project.objects.filter(builder__user=request.user)
        active_projects = projects.filter(status__in=["Planning", "In Progress"])
        overdue_projects = projects.filter(end_date__lt=date.today(), status="In Progress")
        status_choices = dict(Project.STATUS_CHOICES)
        project_status_counts = {status: projects.filter(status=status).count() for status in status_choices.keys()}
    
        context = {
            "active_projects": active_projects.count(),
            "overdue_projects": overdue_projects.count(),
            "project_status_labels": json.dumps(list(status_choices.values())),
            "project_status_counts": json.dumps(list(project_status_counts.values())),
        }
    except Builder.DoesNotExist:
        context = {}
    return render(request, 'user_dashboard.html', context)


def register(request):
    if request.method == 'POST':
        form = BuilderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            Builder.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                contact_info=form.cleaned_data['contact_info'],
                license_number=form.cleaned_data['license_number'],
                area_of_expertise=form.cleaned_data['area_of_expertise']
            )
            
            return redirect('login')
    else:
        form = BuilderRegistrationForm()
    return render(request, 'register.html', {'form': form})

@never_cache
@login_required(login_url='login')
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/login')

@never_cache
@login_required(login_url='login')
def add_client(request):
    builder = Builder.objects.get(user=request.user)
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.builder = builder
            client.save()
            return redirect('/add_client')  
    else:
        form = ClientForm()
        clients = Client.objects.filter(builder__user=request.user)
    return render(request, 'add_client.html', {'form': form,'clients': clients})


@never_cache
@login_required(login_url='login')
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    return redirect('add_client')
    
@never_cache
@login_required(login_url='login')
def update_client(request, client_id):
    client = get_object_or_404(Client, id=client_id, builder__user=request.user)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('add_client')
    else:
        form = ClientForm(instance=client)  
    return render(request, 'update_client.html', {'form': form, 'client': client})
@never_cache
@login_required(login_url='login')
def project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.instance.builder = request.user.builder
            form.save()
            return redirect('project')  
    else:
        form = ProjectForm()
    projects = Project.objects.filter(builder__user=request.user)
    return render(request, 'project.html', {'form': form, 'projects': projects})

@never_cache
@login_required(login_url='login')
def update_project(request, pk):
    project = Project.objects.get(id=pk, builder__user=request.user)
    if request.method == 'POST':
        project.name = request.POST.get('name') 
        project.description = request.POST.get('description')
        client_name = request.POST.get('client')
        client = Client.objects.get(name=client_name)
        project.client = client  
        project.start_date = request.POST.get('start_date')
        project.end_date = request.POST.get('end_date')
        project.status = request.POST.get('status')
        project.budget = request.POST.get('budget')

        project.save() 
        messages.success(request, 'Project updated successfully.')
        return redirect('project')
    else:
        messages.error(request, 'Error updating project. Please check the form data.')
        return redirect('project')
   
    

@login_required(login_url='login')
@never_cache
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project')
