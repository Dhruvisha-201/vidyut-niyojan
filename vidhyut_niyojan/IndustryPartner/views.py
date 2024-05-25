from django.shortcuts import render, redirect
import re
import datetime
from .models import *
from datetime import datetime
from django.db.models import Q
from datetime import date
from django.conf import settings
from vidhyut_niyojan.settings import EMAIL_HOST_USER
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import send_mass_mail   
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.template.loader import render_to_string, get_template
from django.template import Context, Template, RequestContext
from django.core.mail import EmailMessage
import random
from django.contrib import messages
import string
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Count, Sum
from django.urls import reverse
from datetime import datetime

now = datetime.now()

def industry_register(request):
    partner_t = Partner_Type.objects.all()
    states = StateMaster.objects.all()
    city = CityMaster.objects.all()
    
    if request.method == "POST":
        First_Name = request.POST.get('FirstName')
        Last_name = request.POST.get('Lastname')
        Partnertype = request.POST.get('PartnerType')
        Legal_Entity_Name = request.POST.get('LegalEntityName')
        SPOC_Name = request.POST.get('SPOCName')
        SPOC_Email = request.POST.get('SPOCEmail')
        SPOC_Phone = request.POST.get('SPOCPhone')
        Full_Address = request.POST.get('FullAddress')
        State_Name = request.POST.get('StateName')
        District_Name = request.POST.get('DistrictName')
        city = CityMaster.objects.get(City_Name=District_Name)
        PIN_Code = request.POST.get('pincode')
        Office_Phone_No = request.POST.get('OfficePhoneNo')
        Website_Link = request.POST.get('WebsiteLink')
        CreatedDate=datetime.today()
        ModifiedDate=datetime.today()
        passw = request.POST.get('password')
        c_f = request.POST.get('confirm_password')
        
        reg = r'\b^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$\b'
        if(re.fullmatch(reg, passw)):
            if passw == c_f:
                pass
            else:
                messages.error(request,'New Password And Confirm Password Does Not Match', extra_tags = 'navopassword')
                return render(request,"industry-partner-register.html", {'city':city,'partner_t': partner_t,'states':states,"First_N":First_Name,"Last_N":Last_name,"Partner_Type":Partnertype,"Legal_Entity_Name":Legal_Entity_Name,"SPOC_Name":SPOC_Name,"SPOC_Email":SPOC_Email,"Office_Phone_No":Office_Phone_No,"Full_Address":Full_Address,"PIN_Code":PIN_Code,"State_Name":State_Name,"District_Name":District_Name,"SPOC_Phone":SPOC_Phone,"Website_Link":Website_Link})
        else:
            messages.error(request,'Your password is weak, Please including Uppercase, Lowercase, Numbers and Special character', extra_tags = 'pwn')
            return render(request,"industry-partner-register.html", {'city':city,'partner_t': partner_t,'states':states,"First_N":First_Name,"Last_N":Last_name,"Partner_Type":Partnertype,"Legal_Entity_Name":Legal_Entity_Name,"SPOC_Name":SPOC_Name,"SPOC_Email":SPOC_Email,"Office_Phone_No":Office_Phone_No,"Full_Address":Full_Address,"PIN_Code":PIN_Code,"State_Name":State_Name,"District_Name":District_Name,"SPOC_Phone":SPOC_Phone,"Website_Link":Website_Link})

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        registerno = random.randint(100000, 999999)
        if(re.fullmatch(regex, SPOC_Email)):
            pass   
        else:
            messages.error(request,'Please Enter Valid Email', extra_tags = 'e_msg')
            return render(request,"industry-partner-register.html", {'city':city,'partner_t': partner_t,'states':states,"First_N":First_Name,"Last_N":Last_name,"Partner_Type":Partnertype,"Legal_Entity_Name":Legal_Entity_Name,"SPOC_Name":SPOC_Name,"SPOC_Email":SPOC_Email,"Office_Phone_No":Office_Phone_No,"Full_Address":Full_Address,"PIN_Code":PIN_Code,"State_Name":State_Name,"District_Name":District_Name,"SPOC_Phone":SPOC_Phone,"Website_Link":Website_Link})
        if Training_Partner.objects.filter(Contact_Person_Phone=SPOC_Phone).exists() or Industry_partner.objects.filter(SPOC_Phone=SPOC_Phone):
            messages.error(request, "Phone Number is Already Taken, Try With Another Number", extra_tags="phoneverify")
            return render(request,"industry-partner-register.html",{'city':city,'partner_t': partner_t,'states':states,"First_N":First_Name,"Last_N":Last_name,"Partner_Type":Partnertype,"Legal_Entity_Name":Legal_Entity_Name,"SPOC_Name":SPOC_Name,"SPOC_Email":SPOC_Email,"Office_Phone_No":Office_Phone_No,"Full_Address":Full_Address,"PIN_Code":PIN_Code,"State_Name":State_Name,"District_Name":District_Name,"SPOC_Phone":SPOC_Phone,"Website_Link":Website_Link})
        
        elif Training_Partner.objects.filter(Contact_Person_Email=SPOC_Email).exists() or Industry_partner.objects.filter(SPOC_Email=SPOC_Email):
            messages.error(request, "Email is Already Taken, Try With Another", extra_tags="loginverify")
            return render(request,"industry-partner-register.html",{'city':city,'partner_t': partner_t,'states':states,"First_N":First_Name,"Last_N":Last_name,"Partner_Type":Partnertype,"Legal_Entity_Name":Legal_Entity_Name,"SPOC_Name":SPOC_Name,"SPOC_Email":SPOC_Email,"Office_Phone_No":Office_Phone_No,"Full_Address":Full_Address,"PIN_Code":PIN_Code,"State_Name":State_Name,"District_Name":District_Name,"SPOC_Phone":SPOC_Phone,"Website_Link":Website_Link})
        else:
            if passw == c_f:
                Industrypartnercreate = Industry_partner(registerno=registerno,
                                                        First_Name=First_Name, 
                                                        Last_name = Last_name,
                                                        Partner_Type = Partnertype,
                                                        Legal_Entity_Name = Legal_Entity_Name,
                                                        SPOC_Name = SPOC_Name,
                                                        SPOC_Email=SPOC_Email,
                                                        Password=passw,
                                                        SPOC_Phone =SPOC_Phone,
                                                        Full_Address=Full_Address,
                                                        State_Name_id=State_Name,
                                                        District_Name_id=city.id,
                                                        PIN_Code=PIN_Code,
                                                        Office_Phone_No=Office_Phone_No,
                                                        Website_Link=Website_Link,
                                                        IsDeleted= '0',
                                                        IsActive='0',
                                                        CreatedBy=True,
                                                        CreatedDate=CreatedDate,
                                                        ModifiedBy=True,
                                                        ModifiedDate=ModifiedDate)
                Industrypartnercreate.save()         
                                
                                    
                mydict={'email':SPOC_Email,'regno':registerno}
                html_template ='IP_register_mail.html'
                html_message = render_to_string(html_template,context=mydict)
                subject="Welcome To vidhyut_niyojan Applications"
                email_from = EMAIL_HOST_USER

                recipient_list =[SPOC_Email,registerno]
                message=EmailMessage(subject,html_message,email_from,recipient_list)
                message.content_subtype ='html'
                message.send()
                
        
                return redirect('/ip/thank_register/')
            else:
                messages.error(request, 'Password Not Matched', extra_tags='passnot')
                return render(request,"industry-partner-register.html",{'city':city,'partner_t': partner_t,'states':states,"First_N":First_Name,"Last_N":Last_name,"Partner_Type":Partnertype,"Legal_Entity_Name":Legal_Entity_Name,"SPOC_Name":SPOC_Name,"SPOC_Email":SPOC_Email,"Office_Phone_No":Office_Phone_No,"Full_Address":Full_Address,"PIN_Code":PIN_Code,"State_Name":State_Name,"District_Name":District_Name,"SPOC_Phone":SPOC_Phone,"Website_Link":Website_Link})
        
        
    else:  
        states = StateMaster.objects.all()
        return render(request,"industry-partner-register.html",{'states':states,'partner_t': partner_t,'city':city})


def thank_register(request):
    return render(request,'ip_thank_register.html')


def get_register_number(request):              
    if request.method == 'POST':
        regno = request.POST.get('registernumber')

        all_industry_reg = Industry_partner.objects.all()
        for val in all_industry_reg :
            if val.registerno == regno:
                registermo = Industry_partner.objects.get(registerno=regno)
                return render(request,'current_status.html',{'registermo':registermo})
        else:
            messages.error(request,'Please Enter Valid Register Number', extra_tags = 'regno')
            return render(request,'current_status.html')
    else:
        return render(request,'current_status.html')
        

def register_status(request):
    return render(request,'current_status.html')


def industry_login(request):
    if request.method == "POST":
        email = request.POST.get('spocemail')
        passw = request.POST.get('Password')
        # try:
        if Industry_partner.objects.filter(SPOC_Email=email).exists():
            uid = Industry_partner.objects.get(SPOC_Email=email)
            if email == uid.SPOC_Email:
                if passw == uid.Password:
                    request.session['industry_id'] = uid.id
                    request.session['email'] = uid.SPOC_Email
                    messages.error(request, "Successfully Login...!", extra_tags='itag')
                    return redirect('/ip/dashboard/')
                else:
                    messages.error(request, 'Invalid Credential', extra_tags='log')
                    return render(request, 'industry-partner-login.html')
            else:
                messages.error(request, 'Invalid Credential', extra_tags='log')
                return render(request, 'industry-partner-login.html')
        else:
            messages.error(request, 'Invalid Credential',extra_tags='log')
            return render(request, 'industry-partner-login.html')
    else:
        return render(request, "industry-partner-login.html")

def industry_logout(request):
    if 'industry_id'  in request.session:
        logout(request)
        return redirect('/ip/industry_login/')
    else:
        return render(request, 'industry-partner-login.html')


def Dashboard(request):
    """
    - This fun for dashboard 
    """
    # try:
    hired_count = '0'
    decline_count = '0'
    reject_count = '0'
    accept_count = '0'
    candidd = '0'
    user = request.session['industry_id']
    uid = Industry_partner.objects.get(id=user)
    industry_jobpost = Job_Posting.objects.filter(Industry_partner_id=uid)
    all_job = Job_Posting.objects.filter(Industry_partner_id=user).count()
    
    for x in industry_jobpost:
        job_status = Candidate_job_Status.objects.filter(Job_Id=x.id,Job_status=0)
        candidd = Candidate_job_Status.objects.filter(Job_Id=x.id,Job_status=0).count()
        accept_count = Candidate_job_Status.objects.filter(Job_Id=x.id,Job_status=1).count()
        reject_count = Candidate_job_Status.objects.filter(Job_Id=x.id,Job_status=2).count()
        decline_count = Candidate_job_Status.objects.filter(Job_Id=x.id,Job_status=3).count()
        hired_count = Candidate_job_Status.objects.filter(Job_Id=x.id,Job_status=4).count()
       
        return render(request,'index.html',{'all_job': all_job,'uid':uid, 'industry_jobpost':industry_jobpost, 'candidd': candidd, 'hired_count': hired_count,'decline_count':decline_count, 'reject_count':reject_count, 'accept_count':accept_count})
    return render(request,'index.html',{'all_job': all_job,'uid':uid, 'industry_jobpost':industry_jobpost, 'candidd': candidd, 'hired_count': hired_count,'decline_count':decline_count, 'reject_count':reject_count, 'accept_count':accept_count})
    
            
    # except:
    #     messages.error(request,'you have to login first')
    #     return redirect('/ip/industry_login/')
    
def Total_Job_Request(request):
    user = request.session['industry_id']
    uid = Industry_partner.objects.get(id=user)
    all_job = Job_Posting.objects.filter(Industry_partner_id=user)
    candid = []

    for x in all_job:
        candidates = Candidate_job_Status.objects.filter(Job_Id=x.id,Job_status=0)
        
        candid.append(candidates)
        
    return render(request,"Total_job_request.html",{'candid':candid,'uid':uid})

def Total_Job_accept(request):
    user = request.session['industry_id']
    uid = Industry_partner.objects.get(id=user)

    all_job = Job_Posting.objects.filter(Industry_partner_id=user)
    candid = []
    for x in all_job:
        candidates = Candidate_job_Status.objects.filter(Job_Id=x.id,Job_status=1)
        candid.append(candidates)        
    return render(request,"Total_job_accepted.html",{'candid':candid,'uid':uid})

def Total_Job_reject(request):
    user = request.session['industry_id']
    uid = Industry_partner.objects.get(id=user)
    all_job = Job_Posting.objects.filter(Industry_partner_id=user)
    candid = []
    for x in all_job:
        candidates = Candidate_job_Status.objects.filter(Job_Id=x.id,Job_status=2)
        candid.append(candidates)
    return render(request,"Total_job_rejected.html",{'candid':candid,'uid':uid})

def Total_Hired_candidate(request):
    user = request.session['industry_id']
    uid = Industry_partner.objects.get(id=user)
    all_job = Job_Posting.objects.filter(Industry_partner_id=user)
    candid = []
    for x in all_job:
        candidates = Candidate_job_Status.objects.filter(Job_Id=x.id,Job_status=4)
        candid.append(candidates)      
    return render(request,"Total_hired_candidate.html",{'candid':candid,'uid':uid})

def Total_Decline_candidate(request):
    user = request.session['industry_id']
    uid = Industry_partner.objects.get(id=user)
    all_job = Job_Posting.objects.filter(Industry_partner_id=user)
    candid = []
    for x in all_job:
        candidates = Candidate_job_Status.objects.filter(Job_Id=x.id,Job_status=3)
        candid.append(candidates)
    return render(request,"Total_declined_candid.html",{'candid':candid,'uid':uid})

def Total_Job_post(request):
    user = request.session['industry_id']
    uid = Industry_partner.objects.get(id=user)
    all_job = Job_Posting.objects.filter(Industry_partner_id=user)

    return render(request,"Total_job_post.html",{'all_job':all_job,'uid':uid})

def job_posting_list(request):
    try:
        user = request.session['email']
        uid = Industry_partner.objects.get(SPOC_Email=user)
        all_job = Job_Posting.objects.filter(Industry_partner_id=uid.id,IsDeleted=0).order_by('-id')
   
        return render(request,'job_post_view.html',{'uid':uid,'all_job':all_job})
    except:
        messages.error(request,'you have to login first')
        return redirect('/ip/industry_login/')

def completed_candidate(request,id):
    select_candid = Candidate_job_Status.objects.get(Candidate_Id=id)
    select_candid.Job_status = '4'
    select_candid.save()
    job_idd = select_candid.Job_Id
    return HttpResponseRedirect('/ip/applied_candidate/%d'%job_idd.id)

def Decline_candidate(request,id):
    select_candid = Candidate_job_Status.objects.get(Candidate_Id=id)
    select_candid.Job_status = '3'
    select_candid.save()
    job_idd = select_candid.Job_Id
    return HttpResponseRedirect('/ip/applied_candidate/%d'%job_idd.id)

def accept_candidate(request,id):
    select_candid = Candidate_job_Status.objects.get(Candidate_Id=id)
    select_candid.Job_status = '1'
    select_candid.save()
    job_idd = select_candid.Job_Id
    return HttpResponseRedirect('/ip/applied_candidate/%d'%job_idd.id)
 
def reject_candidate(request,id):
    select_candid = Candidate_job_Status.objects.get(Candidate_Id=id)
    select_candid.Job_status = '2'
    select_candid.save()
    job_idd = select_candid.Job_Id
    job_idd.id
    return HttpResponseRedirect('/ip/applied_candidate/%d'%job_idd.id)

    
def applied_candidate(request,id):
    try:
        user = request.session['email']
        uid = Industry_partner.objects.get(SPOC_Email=user)
        all_candidate = Candidate_job_Status.objects.filter(Job_Id = id)
        all_job = Job_Posting.objects.get(id=id)
        return render(request,"selected_candidate.html",{'all_candidate':all_candidate,'all_job':all_job,'uid':uid})
    except:
        messages.error(request,'you have to login first')
        return redirect('/ip/industry_login/')

def job_posting_add(request):
    # try:
    user = request.session['email']
    uid = Industry_partner.objects.get(SPOC_Email=user)
    if request.method=="POST":
        Job_Name = request.POST.get('Job_name')
        Job_type = request.POST.get('Job_type')
        Job_salary = request.POST.get('Job_salary')
        Job_Description = request.POST.get('Job_Description')
        Requirements = request.POST.get('Requirements')
        Number_Of_Requirements = request.POST.get('Number_Of_Requirements')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        Job_Add_Date = request.POST.get('Job_Add_Date')
        country = request.POST.get('country')
        state = request.POST.get('state')
        get_state = StateMaster.objects.get(State_Name=state).id
        city = request.POST.get('city')
        get_city = CityMaster.objects.get(City_Name=city).id
        if not Job_Add_Date:
            Job_Add_Date = None
        Job_Ending_Date = request.POST.get('Job_Ending_Date')
        if not Job_Ending_Date:
            Job_Ending_Date = None
         
        CreatedDate=datetime.today()
        ModifiedDate=datetime.today()
        user = request.session['industry_id']
        uid = Industry_partner.objects.get(id=user)
        jobpostcreate = Job_Posting.objects.create(
            Job_Name=Job_Name,
            Job_type=Job_type,
            Job_salary=Job_salary,
            Job_Description=Job_Description,
            Requirements=Requirements,
            Number_Of_Requirements=Number_Of_Requirements,
            Job_Add_Date=Job_Add_Date,
            Job_Ending_Date=Job_Ending_Date,
            Experience=experience,
            Qualification=qualification,
            Industry_partner_id=uid,
            Country_id_id=country,
            State_id_id=get_state,
            City_id_id=get_city,
            IsActive = "1",
            IsDeleted = "0",
            createby = "vidyut niyojan",
            CreatedDate = CreatedDate,
            ModifiedBy = "vidyut niyojan",
            ModifiedDate = ModifiedDate,
        )
        return redirect("/ip/job_posting_list/",{'uid':uid})
    else:
        countries=CountryMaster.objects.all()
        states=StateMaster.objects.all()
        cities=CityMaster.objects.all()
        return render(request,"job_post_add.html",{'uid':uid,'countries':countries,'states':states,'cities':cities})
    # except:
        # messages.error(request,'you have to login first')
        # return redirect('/ip/industry_login/')  
    
def job_posting_delete(request,id):
    job_post_id = Job_Posting.objects.get(id = id)
    job_post_id.IsDeleted=1            
    job_post_id.save()
    messages.error(request,'Job Post Deleted Successfully', extra_tags = 'jobpostdeleted')

    return redirect("/ip/job_posting_list/")  

def job_posting_update(request,id):
    # try:
        user = request.session['email']
        uid = Industry_partner.objects.get(SPOC_Email=user)
        if request.method == "GET":
            jobpostid = Job_Posting.objects.get(id = id)
            jobpostid_Job_Add_Date=jobpostid.Job_Add_Date
            jobpostid_JobAddDate = jobpostid_Job_Add_Date
            jobpostid_Job_Ending_Date=jobpostid.Job_Ending_Date
            jobpostid_JobEndingDate = jobpostid_Job_Ending_Date
            countries = CountryMaster.objects.all()
            return render(request,"job_post_edit.html",{'countries':countries,'jobpostid':jobpostid,'jobpostid_JobEndingDate':jobpostid_JobEndingDate,'jobpostid_JobAddDate':jobpostid_JobAddDate,'uid':uid})
        
        elif request.method=="POST":
            Job_Name = request.POST.get('Job_Name')
            Job_type = request.POST.get('Job_type')
            Job_salary = request.POST.get('Job_salary')
            Job_Description = request.POST.get('Job_Description')
            Requirements = request.POST.get('Requirements')
            Number_Of_Requirements = request.POST.get('Number_Of_Requirements')
            Job_Add_Date = request.POST.get('Job_Add_Date')
            if not Job_Add_Date:
                Job_Add_Date = None
            Job_Ending_Date = request.POST.get('Job_Ending_Date')
            if not Job_Ending_Date:
                Job_Ending_Date = None
            CreatedDate=datetime.today()
            ModifiedDate=datetime.today()
            experience=request.POST.get('experience')
            qualification=request.POST.get('qualification')
            user = request.session['industry_id']
            uid = Industry_partner.objects.get(id=user)
            jobpostid = Job_Posting.objects.get(id=id)
            jobpostid.Job_Name=Job_Name
            jobpostid.Job_type=Job_type
            jobpostid.Job_salary=Job_salary
            jobpostid.Job_Description=Job_Description
            jobpostid.Requirements=Requirements
            jobpostid.Experience=experience
            jobpostid.Qualification=qualification
            jobpostid.Number_Of_Requirements=Number_Of_Requirements
            jobpostid.Job_Add_Date=Job_Add_Date
            jobpostid.Job_Ending_Date=Job_Ending_Date
            jobpostid.Industry_partner_id=uid
            jobpostid.IsActive = "1"
            jobpostid.IsDeleted = "0"
            jobpostid.createby = "vidyut niyojan"
            jobpostid.CreatedDate = CreatedDate
            jobpostid.ModifiedBy = "vidyut niyojan"
            jobpostid.ModifiedDate = ModifiedDate
            jobpostid.save()
            
                
            
            return redirect("/ip/job_posting_list/")
    # except:
        # messages.error(request,'you have to login first')
        # return redirect('/ip/industry_login/')
    
def search_candidate(request):
    user = request.session['email']
    uid = Industry_partner.objects.get(SPOC_Email=user)
    candidate_search = CandidateMaster.objects.all()
    return render(request,"search-candidate.html",{'candidate_search':candidate_search,'uid':uid})

def get_city(request):
    if request.method == "POST":
        stateinfor = request.POST.get('stateinfo')
        get_element = StateMaster.objects.get(State_Name=stateinfor)
        subject = CityMaster.objects.filter(State_Id = get_element.id)
        statewisecity=list(subject.values())
        
    return JsonResponse({'statewisecity':statewisecity}) 

statewisecity = '[]'
def new_get_city_ajax(request):
    if request.method == "POST":
        stateinfor = request.POST['stateinfo']

        subject = CityMaster.objects.filter(State_Id=stateinfor)

        statewisecity = list(subject.values())
        print(type(statewisecity))
    return JsonResponse({'statewisecity': statewisecity})


countrystate = '[]'
def get_state(request):
    if request.method == "POST":
        countryinfo = request.POST['countryinfo']
        subject = StateMaster.objects.filter(country_Id = countryinfo)
        countrystate=list(subject.values())
    return JsonResponse({'countrystate':countrystate}) 
   

def Filter_candidate(request):
    all_job = Job_Posting.objects.all()
    user = request.session['email']
    uid = Industry_partner.objects.get(SPOC_Email=user)
    states = StateMaster.objects.all()
    Cource = CourceMaster.objects.all()
    city = CityMaster.objects.all()
    if ('q' in request.GET) or ('findstate' in request.GET) or ('findcity' in request.GET):
        value = request.GET.get('q', '').split(" ")
        fin = CandidateMaster.objects.filter(Job_Name__icontains=value[0])
        my_value = []
        for val in fin:
            value = request.GET.get('findstate')
            find_city = request.GET.get('findcity')
            filter_find_city = CityMaster.objects.get(City_Name=find_city).id
            if value == '' : 
                my_value.append(val)
            elif int(value) == val.State_Id.id:
                my_value.append(val)
            elif filter_find_city == val.City_Id.id:
                my_value.append(val)
            else:
                pass
        
        return render(request,"filter-candidate.html",{'states':states, 'my_value': my_value, 'uid': uid, 'all_job': all_job, 'city': city})
    return render(request,"filter-candidate.html",{'states':states, 'uid': uid, 'all_job': all_job, 'city': city})


def contact_us(request):
    user = request.session['industry_id']
    uid = Industry_partner.objects.get(id=user)
    return render(request,'contact_us.html', {'uid': uid})


def ip_settings(request):
    return render(request,'setting.html')


def common_data(list1, list2):
    result = False

    # traverse in the 1st list
    for x in list1:

        # traverse in the 2nd list
        for y in list2:
    
            # if one common
            if x == y:
                result = True
                return result 
                
    return result

def IP_profile(request):
    try:
        user = request.session['email']
        uid = Industry_partner.objects.get(SPOC_Email=user)
        Ip_View_Profile = Industry_partner.objects.get(id = request.session['industry_id'])
        return render(request,"IP_profile.html",{'Ip_View_Profile':Ip_View_Profile,'uid':uid})
    except:
        messages.error(request,'you have to login first')
        return redirect('/ip/industry_login/')

def IP_Update_Profile(request):
    try:
        state = StateMaster.objects.all()
        user = request.session['industry_id']
        uid = Industry_partner.objects.get(id=user)
        if request.method == "GET":
            Ip_Select_Profile = Industry_partner.objects.get(id = request.session['industry_id'])
            return render(request,"edit_IP_profile.html",{'Ip_Select_Profile':Ip_Select_Profile,'uid':uid, 'state': state})
        elif request.method == "POST":
            First_Name = request.POST.get('FirstName')
            Last_name = request.POST.get('Lastname')
            Partner_Type = request.POST.get('PartnerType')
            Legal_Entity_Name = request.POST.get('LegalEntityName')
            SPOC_Name = request.POST.get('SPOCName')
            spocemail  = request.POST.get('SPOCEmail')
            newvar = Industry_partner.objects.filter(SPOC_Email=spocemail).count()
            SPOC_Phone = request.POST.get('SPOCPhone')
            Full_Address = request.POST.get('FullAddress')
            State_Name = request.POST.get('StateName')
            District_Name = request.POST.get('DistrictName')
            PIN_Code = request.POST.get('pincode')
            Office_Phone_No = request.POST.get('OfficePhoneNo')
            Website_Link = request.POST.get('WebsiteLink')
            state = StateMaster.objects.all()
            user = request.session['industry_id']
            uid = Industry_partner.objects.get(id=user)
            Ip = Industry_partner.objects.all()
            user_id = []
            Email_List = []
            for val in Ip:
                user_id.append([val.id,val.SPOC_Email])
            for i in user_id:
                if i[0] == request.session['industry_id'] and i[1] == spocemail:
                    print('hiii')
                else:
                    Email_List.append(str(i[1]))
            Email_one_good = [spocemail]
            if common_data(Email_List, Email_one_good)==True:
                messages.error(request,  'Already Taken, Try with Different Email', extra_tags='editverify')
                Ip_Select_Profile = Industry_partner.objects.get(id = request.session['industry_id'])
                return render(request,"edit_IP_profile.html",{'Ip_Select_Profile':Ip_Select_Profile,'uid':uid, 'state': state})
            else:
                Ip_View_Profile = Industry_partner.objects.get(id = request.session['industry_id'])
                Ip_View_Profile.First_Name=First_Name
                Ip_View_Profile.Last_name=Last_name
                Ip_View_Profile.Partner_Type=Partner_Type
                Ip_View_Profile.Legal_Entity_Name=Legal_Entity_Name
                Ip_View_Profile.SPOC_Name=SPOC_Name
                Ip_View_Profile.SPOC_Email = spocemail
                request.session['email'] = spocemail
                Ip_View_Profile.SPOC_Phone = SPOC_Phone
                Ip_View_Profile.Full_Address = Full_Address
                SState = StateMaster.objects.get(State_Name=State_Name)
                Ip_View_Profile.State_Name_id = SState.id
                CCity = CityMaster.objects.get(City_Name=District_Name)
                Ip_View_Profile.District_Name_id = CCity.id
                Ip_View_Profile.PIN_Code = PIN_Code
                Ip_View_Profile.Office_Phone_No = Office_Phone_No
                Ip_View_Profile.Website_Link = Website_Link
                Ip_View_Profile.save()
                return redirect('/ip/IP_profile')
    except:
        messages.error(request, 'you have to login first')
        return redirect('/ip/industry_login/')
    
def forgat_password(request):
    user = request.session['email']
    uid = Industry_partner.objects.get(SPOC_Email=user)
    return render(request,"forgot_password.html", {'uid': uid})

def change_password(request):

    mes = ''
    mes += f"Password Should Contain atleast 1 Special character"

    user = request.session['email']
    uid = Industry_partner.objects.get(SPOC_Email=user)
    if request.method == "POST":
        old_password=request.POST.get('oldpass')
        newpassw=request.POST.get('newpassword')
        confirmpassw=request.POST.get('confirmpassword')
        if uid.Password == old_password:
            regex = r'\b^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$\b'
            if (re.fullmatch(regex, newpassw)):
                pass 
                if newpassw == confirmpassw:
                    uid.Password = newpassw
                    uid.save()
                    return redirect('/ip/IP_profile/')
                else:
                    messages.error(request, 'New Password And Confirm Password Does Not Match', extra_tags = 'newpasss')
                    return render(request, "change_password.html",{'uid':uid})
            else:
                messages.error(request, 'Your password is weak, Please including Uppercase, Lowercase, Numbers and Special character', extra_tags = 'passwordw')
                return render(request, "change_password.html",{'uid':uid})
        else:
            messages.error(request, 'Please Enter Valid Old Password', extra_tags = 'oldpassword')
            return render(request, "change_password.html",{'uid':uid})
    else:
        return render(request, "change_password.html",{'uid':uid})
    
def RPL_List(request):
    user = request.session['email']
    uid = Industry_partner.objects.get(SPOC_Email=user)
    RPL_data = RPL_Master.objects.filter(Industry_partner_Id=uid,Is_deleted=0)
    return render(request,"RPL_List.html",{'uid':uid,'RPL_data':RPL_data})

def RPL_delete(request,id):
    RPL_delete = RPL_Master.objects.get(id=id)
    RPL_delete.Is_deleted=1
    RPL_delete.save()
    messages.error(request, 'RPL Successfully Deleted', extra_tags = 'RPLdelete')
    return redirect("/ip/RPL_List/")

def IP_RPL(request):
    user = request.session['email']
    uid = Industry_partner.objects.get(SPOC_Email=user)
    if request.method == "GET":
        countries=CountryMaster.objects.all()
        job_role=Job_Posting.objects.all()
        return render(request,"RPL.html",{'countries':countries,'uid':uid,'job_role':job_role})
    
    elif request.method == "POST":
        training_type=request.POST['training_type']
        job_role=request.POST['job_role']
        SPOC_name=request.POST['SPOC_name']
        SPOC_number=request.POST['SPOC_number']
        SPOC_Email=request.POST['SPOC_Email']
        SPOC_designation=request.POST['SPOC_designation']
        Target=request.POST['Target']
        Area=request.POST['Area']
        country=request.POST['country']
        countries=CountryMaster.objects.get(id=country)
        state=request.POST['state']
        states=StateMaster.objects.get(State_Name=state)
        DistrictName=request.POST['city']
        cities=CityMaster.objects.get(City_Name=DistrictName)
        Pincode=request.POST['Pincode']
        
        RPL_Master.objects.create(
            Industry_partner_Id= uid,
            Trining_type=training_type,
            Job_role=job_role,
            Target=Target,
            Area=Area,
            Country_Id=countries,
            State_Id=states,
            City_Id=cities,
            pincode=Pincode,
            SPOC_Name=SPOC_name,
            SPOC_Number=SPOC_number,
            SPOC_Email=SPOC_Email,
            SPOC_Designation=SPOC_designation,
            Is_deleted=0,
            IsActive=0
        )
        messages.error(request, 'Data Inserted', extra_tags='datainsert')
        
        return redirect('/ip/RPL_List/')
        