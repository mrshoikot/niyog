from datetime import datetime
from re import L
from unicodedata import category, name
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
import django
from .models import Job, Category, UserJob, Role
from django.core.files.storage import FileSystemStorage

def index(request):
    role = Role.objects.get(user=request.user).type if request.user.is_authenticated else ""

    context = {
        'role': role,
    }
    return render(request,'index.html' ,context)

def joblist(request):
    return render(request,'categories.html')

def postjob(request):
    is_approved = Role.objects.get(user=request.user).is_approved if request.user.is_authenticated else False

    context = {
        'is_approved': is_approved,
    }
    if request.user.is_authenticated:
        return render(request,'postjob.html', context)
    else:
        messages.info(request,'Please SignIn or Log In First')
        return redirect('auth')

def jobs(request):
    posts=Job.objects.filter(category__name=request.GET['category'])
    #print(request.GET['deadline'])
    if posts:
        return render(request,'jobs.html', {'name':request.GET['category'],'jobs':posts})
    else:
        return HttpResponse('<h1>no jobs in this category</h1>')

def company_registration(request):
    return render(request,'company_registration.html')

def mechanic(request):
    return render(request,'mechanic.html')

def food(request):
    return render(request,'mechanic.html')

def driver(request):
    return render(request,'driver.html')

def medical(request):
    return render(request,'medical.html')

def auth(request):
    return render(request,'signlog.html')

def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        if request.user.is_authenticated:
            messages.info(request,'You are already log in')
            return redirect('auth')
        else:
            username = User.objects.get(email=email).username
            user = authenticate(username=username,password=password)

            if user:
                django.contrib.auth.login(request, user)
                return redirect('index')
            else:    
                messages.info(request,'Invalid Credentials')
                return redirect('auth')


def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['confirmpassword']

        if password==confirmpassword:
            if User.objects.filter(email=email).exists():
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Both Email and username already used')
                    return redirect('auth')
                else:
                    messages.info(request,'Email already used')
                    return redirect('auth')
            elif User.objects.filter(username=username):
                messages.info(request,'username is already used')
                return redirect('auth')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password)
                user.save()

                Role.objects.create(user=user, type=request.POST['role'])

                messages.info(request,'Sign Up Successfully')
                return redirect('auth')
        else:
            messages.info(request,'Password does not match')
            return redirect('auth')


def logout(request):
    if request.user.is_authenticated:
        django.contrib.auth.logout(request)
        return redirect('index')
    else:
        return render(request,'signlog.html',{'pk':'logout'})



def job(request):
        if request.method == 'POST':
            category = Category.objects.get_or_create(name=request.POST['category'])[0]
            print(category)
            job = Job()
            job.company=request.POST['company']
            job.post=request.POST['post']
            job.location=request.POST['location']
            job.deadline=request.POST['deadline']
            job.details=request.POST['details']
            job.category = category
            job.user_id = request.user.id
            job.save()
            return redirect('postjob')
    







def apply(request, job_id):
    if request.user.is_authenticated:
        job = Job.objects.get(id=job_id)
        print(job)
        if request.method == 'GET':
            if UserJob.objects.filter(user=request.user, job=job).exists():
                return HttpResponse('<h1>already applied</h1>')
            else:
                return render(request,'apply.html', {"job": job})
        elif request.method == 'POST':
            UserJob.objects.create(user=request.user, job=job, cv=request.FILES['cv'])
            messages.info(request,'Successfully Applied')
            return redirect('auth')
            # return render(request,'apply.html', {"job": job})
    else:
        messages.info(request,'SignIn Required')
        return redirect('auth')








def applicants(request):
    #request.user.jobs.applicant
    if request.user.is_authenticated:
        print(request.user.id)
        jobs = Job.objects.filter(user_id=request.user.id)
        applicants = []
        print(type(jobs))
        for job in jobs:
            middles = job.applicants.through.objects.all()
            print(len(jobs))
            print(len(middles))
            for row in middles:
                print("inside for loop")
                user = row.user
                user.cv = row.cv
                applicants.append(user)
            break
        return render(request,'applicants.html', {'applicants': applicants})
    else:
        return redirect('auth')     