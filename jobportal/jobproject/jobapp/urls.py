from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('jobs/', views.all_jobs, name='all_jobs'),
    path('job/<int:job_id>/applications/', views.view_applications, name='view_applications'),
    path('post-job/', views.post_job, name='post_job'),
    path('add-job/', views.add_job, name='add_job'),
    path('job/<slug:slug>/', views.job_detail, name='job_detail'), 
    path('job/<slug:slug>/apply/', views.apply_job, name='apply_job'),
    


]

