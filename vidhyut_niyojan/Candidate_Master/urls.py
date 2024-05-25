from django.contrib import admin
from django.urls import path
from Candidate_Master import views

app_name = "Candidate_Master"
      

urlpatterns = [
    path('',views.candidate_login,name="candidate_login"),
    path('Candidate_register/',views.Candid_register, name="Candidate_register"),
    path('candidate_logout',views.candidate_logout,name="candidate_logout"),
    
    path('candidate_dashboard/',views.candidate_dashboard,name="candidate_dashboard"),
    
    path('candidate_profile/',views.candidate_profile,name="candidate_profile"),
    path('change_password/',views.change_password,name="change_password"),
    path('CM_Update_Profile/',views.CM_Update_Profile,name="CM_Update_Profile"),
    
    path('all_job_post/',views.all_job_post,name="all_job_post"),
    path('job_details/<int:id>',views.job_details,name="job_details"),
    
    path('candidate_apply_job/<int:id>',views.candidate_apply_job,name="candidate_apply_job"),

    
    path('resume_build/', views.resume_build),
    path('add_skill/', views.add_skill),
    path('add_edu/', views.add_edu),
    path('add_family/', views.add_family),
    path('add_exp/', views.add_exp),
    path('download_resume/', views.download_resume),
    path('filter_job/', views.filter_job, name='filter_job')
    
    
    
    
]