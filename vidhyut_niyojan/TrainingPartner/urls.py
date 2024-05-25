from django.urls import path
from TrainingPartner import views

app_name = 'TrainingPartner'

urlpatterns = [
    path('', views.training_register,name="training_register"),
    path('training_login/',views.training_login,name="training_login"),
    path('get_reg_number/',views.get_reg_number,name="get_reg_number"),
    path('training_dashboard/',views.training_dashboard,name ="training_dashboard"),
    path('training_logout/',views.training_logout, name="training_logout"),
    path('add_training_center/',views.add_training_center, name="add_training_center"),
    path('edit_center/<int:id>/',views.edit_center,name="edit_center"),
    path('delete_center/<int:id>/',views.delete_center),
    path('center_list/',views.center_list,name="center_list" ),
    path('add_candidate/',views.add_candidate,name='add_candidate'),
    path('candidate_list/',views.candidate_list,name="candidate_list"),
    path('edit_candidate/<int:id>/',views.edit_candidate,name="edit_candidate"),
    path('delete_candidate/<int:id>/',views.delete_candidate),
    path('training_setting/',views.training_setting,name="training_setting"),
    path('trainig_contact_us/',views.trainig_contact_us,name="trainig_contact_us"),
    path('TP_profile/',views.TP_profile,name="TP_profile"),
    path('TP_Update_Profile/',views.TP_Update_Profile,name="TP_Update_Profile"),
    path('change_passwor/',views.change_passwor,name="change_passwor"),
    path('bulkupload/',views.bulkupload,name="bulkupload"),
    path('delete_bulk/<int:id>/',views.delete_bulk,name="delete_bulk"),
    path('view_job_post/',views.view_job_post,name="view_job_post"),
    path('get_city_ajax/',views.get_city_ajax,name="get_city_ajax"),
    path('job_details/<int:id>/',views.job_details,name="job_details"),
    path('candidate_apply_job/<int:id>/',views.candidate_apply_job,name="candidate_apply_job"),
    path('apply_job/<int:id>',views.apply_job,name="apply_job"),
    path('apply_candid_job/',views.apply_candid_job,name="apply_candid_job"),
    path('thank/',views.thank,name="thank"),
    path('view_applied_candidate/<int:id>/',views.view_applied_candidate,name="view_applied_candidate"),
    path('loginverify/', views.loginverify)






]