from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Job, EmployerProfile
from .forms import JobForm, ApplicationForm
from django.utils.text import slugify
import uuid


def home(request):
    jobs = Job.objects.all()
    return render(request, 'jobapp/home.html', {'jobs': jobs})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'jobapp/login.html', {'error': 'Invalid Credentials'})

    return render(request, 'jobapp/login.html')

# def user_login(request):
#     error = None
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # Authenticate user
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)

#                 # Redirect based on user type
#                 if hasattr(user, 'employerprofile'):
#                     return redirect('add_job')      # Employer dashboard/add job
#                 elif hasattr(user, 'jobseekerprofile'):
#                     return redirect('job_list')     # Job seeker dashboard
#                 elif user.is_superuser:
#                     return redirect('/admin/')      # Admin redirect
#                 else:
#                     return redirect('home')         # Default redirect
#             else:
#                 error = "This account is inactive."
#         else:
#             error = "Invalid username or password"

#     return render(request, 'jobapp/login.html', {'error': error})


def user_logout(request):
    logout(request)
    return redirect('login')


# POST NEW JOB

@login_required
def post_job(request):
    try:
        employer = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return redirect('create_employer_profile')   # add your URL name

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.slug = slugify(job.title) + "-" + str(uuid.uuid4())[:8]
            job.save()
            return redirect('my_jobs')
    else:
        form = JobForm()

    return render(request, 'jobapp/post_job.html', {'form': form})


# EMPLOYER'S POSTED JOBS

@login_required
def my_jobs(request):
    try:
        employer = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return redirect('create_employer_profile')

    jobs = Job.objects.filter(employer=employer)
    return render(request, 'jobapp/my_job.html', {'jobs': jobs})


# VIEW APPLICATIONS FOR A JOB

@login_required
def view_applications(request, job_id):
    try:
        employer = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return redirect('create_employer_profile')

    job = get_object_or_404(Job, id=job_id, employer=employer)
    applications = job.applications.all()

    return render(request, 'jobapp/view_application.html', {
        'job': job,
        'applications': applications
    })


# ALL JOBS PAGE (WITH SEARCH)

def all_jobs(request):
    q = request.GET.get("q", "")
    if q:
        jobs = Job.objects.filter(title__icontains=q)
    else:
        jobs = Job.objects.all()

    return render(request, "jobapp/all_job.html", {"jobs": jobs})

@login_required
# def apply_job(request, slug):
#     job = get_object_or_404(Job, slug=slug)

#     if request.method == "POST":
#         form = ApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             application = form.save(commit=False)
#             application.job = job
#             application.save()
#             return render(request, 'jobapp/application_success.html', {'job': job})
#     else:
#         form = ApplicationForm()

#     return render(request, 'jobapp/apply_job.html', {'job': job,'form': form})

# views.py
# from django.shortcuts import render

def add_job(request):
    return render(request, 'jobapp/add_job.html')

def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    return render(request, 'jobapp/job_detail.html', {'job': job})

# def apply_job(request, slug):
#     job = get_object_or_404(Job, slug=slug)

#     if request.method == "POST":
#         form = ApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             application = form.save(commit=False)
#             application.job = job
#             application.save()
#             return redirect('job_detail', slug=slug)  
#     else:
#         form = ApplicationForm()

#     return render(request, 'jobapp/apply_job.html', {
#         "job": job,
#         "form": form,
#     })


def apply_job(request, slug):
    job = get_object_or_404(Job, slug=slug)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()

            return render(request, "jobapp/application_success.html", {"job": job})
    else:
        form = ApplicationForm()

    return render(request, "jobapp/apply_job.html", {"form": form, "job": job})




