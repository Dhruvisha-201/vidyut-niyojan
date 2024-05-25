from django.urls import path
from . import views

app_name = "vidhyut_Admin"

urlpatterns = [
    path('admin_index/', views.admin_index),
    path('admin_logout/', views.admin_logout),
    path('adlogin/', views.adlogin),
    path('industry_list/', views.industry_list, name='industry_list'),
    path('training_list/', views.training_list, name='training_list'),
    path('add_industry/', views.add_industry, name='add_industry'),
    path('companyaccept/<int:id>/', views.companyaccept, name='companyaccept'),
    path('companyreject/<int:id>/', views.companyreject, name='companyreject'),
    path('edit_industry/<int:id>/', views.edit_industry, name='edit_industry'),
    path('delete_industry/<int:id>/', views.delete_industry, name='delete_industry'),
    path('edit_training/<int:id>/', views.edit_training, name='edit_training'),
    path('edit_center/<int:id>/', views.edit_center, name='edit_center'),
    path('delete_training/<int:id>/', views.delete_training, name='delete_training'),
    path('add_trainig/', views.add_trainig, name='add_trainig'),
    path('add_training_center/', views.add_training_center, name='add_training_center'),
    path('list_center/', views.list_center, name='list_center'),
    path('trainingAccept/<int:id>/', views.trainingAccept, name='trainingAccept'),
    path('trainingreject/<int:id>/', views.trainingreject, name='trainingreject'),
    path('centerAccept/<int:id>/', views.centerAccept, name='centerAccept'),
    path('centerReject/<int:id>/', views.centerReject, name='centerReject'),
    path('delete_center/<int:id>/', views.delete_center, name='delete_center'),
    path('admin_rpl_list/', views.admin_rpl_list, name='admin_rpl_list'),
    path('rpl_deleted/<int:id>/', views.rpl_deleted, name='rpl_deleted'),
    path('get_city_admin/', views.get_city_admin, name='get_city_admin'),
    path('setting/', views.setting, name='setting'),
    path('add_job/', views.add_job, name='add_job'),
    path('jobfairlist/', views.jobfairlist, name='jobfairlist'),
    path('edit_jobfair/<int:id>/', views.edit_jobfair, name='edit_jobfair'),
    path('delete_jobfair/<int:id>/', views.delete_jobfair, name='delete_jobfair'),




    
]