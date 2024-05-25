from django.contrib import admin
from django.urls import path
from IndustryPartner import views

app_name = "IndustryPartner"
      

urlpatterns = [
    path('',views.industry_register,name="industry_register"),
    path('thank_register/',views.thank_register,name="thank_register"),
    path('register_status/',views.register_status,name="register_status"),
    path('get_register_number/',views.get_register_number,name="get_register_number"),
    path('industry_login/',views.industry_login,name="industry_login"),
    path('industry_logout/',views.industry_logout,name="industry_logout"),
    
    path('dashboard/',views.Dashboard,name="dashboard"),
    path('Total_Job_Request/',views.Total_Job_Request,name="Total_Job_Request"),
    path('Total_Job_accept/',views.Total_Job_accept,name="Total_Job_accept"),
    path('Total_Job_reject/',views.Total_Job_reject,name="Total_Job_reject"),
    path('Total_Hired_candidate/',views.Total_Hired_candidate,name="Total_Hired_candidate"),
    path('Total_Decline_candidate/',views.Total_Decline_candidate,name="Total_Decline_candidate"),
    path('Total_Job_post/',views.Total_Job_post,name="Total_Job_post"),
    
    path('job_posting_list/',views.job_posting_list,name="job_posting_list"),
    path('job_posting_add/',views.job_posting_add,name="job_posting_add"),
    path('job_posting_update/<int:id>',views.job_posting_update,name="job_posting_update"),
    path('job_posting_delete/<int:id>',views.job_posting_delete,name="job_posting_delete"),
    
    path('search_candidate/',views.search_candidate,name="search_candidate"),
    path('get_city/',views.get_city,name="get_city"),
    path('new_get_city_ajax/',views.new_get_city_ajax,name="new_get_city_ajax"),
    path('get_state/',views.get_state,name="get_state"),
    path('Filter_candidate/',views.Filter_candidate,name="Filter_candidate"),
    path('contact_us/',views.contact_us,name="contact_us"),
    path('ip_settings/',views.ip_settings,name="ip_settings"),
    
    path('IP_profile/',views.IP_profile,name="IP_profile"),
    path('IP_Update_Profile/',views.IP_Update_Profile,name="IP_Update_Profile"),
    path('forgat_password/',views.forgat_password,name="forgat_password"),
    path('change_password/',views.change_password,name="change_password"),
    
    path('applied_candidate/<int:id>',views.applied_candidate, name="applied_candidate"),
    path('IP_RPL/',views.IP_RPL, name="IP_RPL"),
    path('RPL_List/',views.RPL_List, name="RPL_List"),
    path('RPL_delete/<int:id>',views.RPL_delete, name="RPL_delete"),
    
    path('completed_candidate/<int:id>',views.completed_candidate, name="completed_candidate"),
    path('Decline_candidate/<int:id>',views.Decline_candidate, name="Decline_candidate"),
    path('accept_candidate/<int:id>',views.accept_candidate, name="accept_candidate"),
    path('reject_candidate/<int:id>',views.reject_candidate, name="reject_candidate"),
    
    
    
]