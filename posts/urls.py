from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('categories',views.joblist,name='joblist'),
    path('postjob',views.postjob,name='postjob'),
    path('jobs',views.jobs,name='art'),
    path('driver',views.driver,name='driver'),
    path('mechanic',views.mechanic,name='mechanic'),
    path('medical',views.medical,name='medical'),
    path('food',views.food,name='food'),
    path('auth',views.auth,name='auth'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('job',views.job,name='job'),
    path('application/<int:job_id>',views.apply,name='apply'),
    path('applicants',views.applicants,name='applicants'),
    path('company_registration',views.company_registration,name='company_registration'),
]