from django.shortcuts import render
from TrainingPartner.models import Training_Partner
from IndustryPartner.models import Industry_partner
# Create your views here.


def PSSC_HOME(request):
    TP = Training_Partner.objects.all().count()
    IP = Industry_partner.objects.all().count()
    return render(request, "home.html", {'TP': TP, 'IP': IP})

def contact_us(request):
    return render(request , 'contact.html')