from django.contrib import admin
from django.urls import path
from Home import views

app_name = "Home"

urlpatterns = [
    path('', views.PSSC_HOME, name="PSSC_HOME"),
    path('contact_us/', views.contact_us, name="contact_us"),
]
