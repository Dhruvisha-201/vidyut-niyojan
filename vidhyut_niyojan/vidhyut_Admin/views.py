
from http.client import HTTPResponse
import re
from django.shortcuts import render, redirect
from django.contrib import messages
import random
from IndustryPartner.models import Industry_partner, RPL_Master
from TrainingPartner.models import CityMaster, Training_Partner, Training_center, StateMaster, CandidateMaster
from .models import admin
# Create your views here.
import string
from django.conf import settings
from vidhyut_niyojan.settings import EMAIL_HOST_USER
from django.core.mail import BadHeaderError, send_mail
from datetime import datetime
from django.core.mail import send_mass_mail, EmailMessage
from django.template.loader import render_to_string, get_template
from vidhyut_niyojan.settings import EMAIL_HOST_USER
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string, get_template
from django.template import Context, Template, RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse

def adlogin(request):
    if request.method == "POST":
        email = request.POST.get('username')
        passw = request.POST.get('password')
        try:
            uid = admin.objects.get(UserName=email)
            if email == uid.UserName:
                
                if passw == uid.Password    :
                    request.session['admin_id'] = uid.id
                    request.session['username'] = uid.UserName
                    return redirect('/ad/admin_index/')
                else:
                    messages.error(request,'Invalid Email Or Password', extra_tags='logemail')
                    return render(request,'adminlogin.html')
            else:
                messages.error(request,'Invalid Email Or Password', extra_tags='logemail')
                return render(request, 'adminlogin.html')
        except :
            messages.error(request,'Invalid Email Or Password', extra_tags='emailnorpass')
            return render(request, 'adminlogin.html')   
    else:
        pass
    return render(request,"adminlogin.html")


def admin_logout(request):
    if 'admin_id' in request.session:
        logout(request)
    return redirect('/ad/adlogin/')

def admin_header(request):
    try:
        ids = request.session['admin_id']
        admin_data = admin.objects.all()
        return render(request, 'admin_index.html')
    except:
        return redirect('/ad/admin_login/')

def admin_index(request):
    try:
        ids = request.session['admin_id']
        industry = Industry_partner.objects.all().count()
        training = Training_Partner.objects.all().count()
        center = Training_center.objects.all().count()
        candidate = CandidateMaster.objects.all().count()
        total_rpl = RPL_Master.objects.all().count()
        ids = request.session['admin_id']
        admin_data = admin.objects.get(id=ids)
        adminname = admin_data.First_name
        return render(request, 'admin_index.html', {'industry':industry, 'training':training, 'center':center, 'adminname':adminname, 'candidate':candidate, 'total_rpl': total_rpl})
    except :
        messages.error(request, 'You have to login first')
        return redirect('/ad/adlogin/')

# INDUSTRY PARTNER

def industry_list(request):
    try:
        ids = request.session['admin_id']
        admin_data = admin.objects.get(id=ids)
        adminname = admin_data.First_name
        ids = request.session['admin_id']
        industry = Industry_partner.objects.all().order_by('-id')
        return render(request,'industrylist.html', {'industry': industry, 'adminname': adminname})
    except :
        return redirect('/ad/adlogin/')

def add_industry(request):
    # try:
        ids = request.session['admin_id']
        admin_data = admin.objects.get(id=ids)
        adminname = admin_data.First_name
        s = StateMaster.objects.all()
        c = CityMaster.objects.all()


        if request.method == 'POST':
            First_Name = request.POST.get('First_Name')
            Last_name = request.POST.get('Last_name')
            Partner_Type = request.POST.get('Partner_Type')
            Legal_Entity_Name = request.POST.get('Legal_Entity_Name')
            SPOC_Name = request.POST.get('SPOC_Name')
            SPOC_Email = request.POST.get('SPOC_Email')
            SPOC_Phone = request.POST.get('SPOC_Phone')
            Full_Address = request.POST.get('Full_Address')
            State_Name = request.POST.get('State_Name')
            District_Name = request.POST.get('District_Name')
            PIN_Code = request.POST.get('PIN_Code')
            Office_Phone_No = request.POST.get('Office_Phone_No')
            Website_Link = request.POST.get('Website_Link')
            CreatedDate=datetime.now()
            ModifiedDate=datetime.now()
            registerno = random.randint(1000000000, 9999999999)
            loginPassword = request.POST.get('Password')
            regex = r'[a-z0-9.A-Z]+@gmail.com'
            if Industry_partner.objects.filter(SPOC_Email=SPOC_Email).exists():
                messages.error(request, "Already Taken, Try With Another mail", extra_tags='aipv')
                return render(request, 'add_indutry.html', {'s':s, 'c':c,'First_Name': First_Name, 'Last_name': Last_name, 'Partner_Type' :Partner_Type, 'Legal_Entity_Name' :Legal_Entity_Name,
                    'SPOC_Name' :SPOC_Name, 'SPOC_Phone' :SPOC_Phone, 'Full_Address' : Full_Address,'State_Name' :State_Name, 'District_Name' :District_Name, 'PIN_Code': PIN_Code, 'Office_Phone_No':Office_Phone_No, 'Website_Link': Website_Link})
            else:
                
                Industrypartnercreate = Industry_partner(registerno=registerno,
                                                        First_Name=First_Name, 
                                                        Last_name = Last_name,
                                                        Partner_Type = Partner_Type,
                                                        Legal_Entity_Name = Legal_Entity_Name,
                                                        SPOC_Name = SPOC_Name,
                                                        SPOC_Email=SPOC_Email,
                                                        Password=loginPassword,
                                                        SPOC_Phone =SPOC_Phone,
                                                        Full_Address=Full_Address,
                                                        State_Name_id=State_Name,
                                                        District_Name_id=District_Name,
                                                        PIN_Code=PIN_Code,
                                                        Office_Phone_No=Office_Phone_No,
                                                        Website_Link=Website_Link,
                                                        IsDeleted= '0',
                                                        IsActive='1',
                                                        CreatedBy=True,
                                                        CreatedDate=CreatedDate,
                                                        ModifiedBy=True,
                                                        ModifiedDate=ModifiedDate
                                                        )

                                                        
                mydict={'email':SPOC_Email,'regno':loginPassword}
                html_template ='credential.html'
                html_message = render_to_string(html_template,context=mydict)
                subject="Welcome To Vidhyut Niyojan Applications"
                email_from = EMAIL_HOST_USER

                recipient_list =[SPOC_Email,loginPassword]
                message=EmailMessage(subject,html_message,email_from,recipient_list)
                message.content_subtype ='html'
                message.send()
                                
                Industrypartnercreate.save()  
                messages.error(request,'Industry Inserted Successfully', extra_tags = 'indusadd')
                print('Industrypartnercreate', Industrypartnercreate)
                return redirect('/ad/industry_list/')
        

        return render(request, 'add_indutry.html', {'adminname': adminname,'s':s, 'c':c})
    # except:
    #     return redirect('/ad/adlogin/')

def companyaccept(request, id):
    
    company = Industry_partner.objects.get(id=id)

    loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

    mydict={'email':company.SPOC_Email,'regno':company.Password}
    html_template ='admin_mail_thanks.html'
    html_message = render_to_string(html_template,context=mydict)
    subject="Welcome To Vidhyut Niyojan Applications"
    email_from = EMAIL_HOST_USER

    recipient_list =[company.SPOC_Email,company.Password]
    message=EmailMessage(subject,html_message,email_from,recipient_list)
    message.content_subtype ='html'
    message.send()

    company.IsActive = '1'
    company.save()
    messages.error(request,'Industry Partner Accepted', extra_tags = 'acceptindus')

    return redirect('/ad/industry_list/')

def companyreject(request,id): 
    
    deletecompany = Industry_partner.objects.get(id=id)

    mydict={'email':deletecompany.SPOC_Email,'regno':deletecompany.Password}
    html_template ='reject.html'
    html_message = render_to_string(html_template,context=mydict)
    subject="Welcome To Vidhyut Niyojan Applications"
    email_from = EMAIL_HOST_USER

    recipient_list =[deletecompany.SPOC_Email]
    message=EmailMessage(subject,html_message,email_from,recipient_list)
    message.content_subtype ='html'
    message.send()
    deletecompany.IsActive = 2
    deletecompany.save()
    messages.error(request,'Industry Partner Rejected', extra_tags = 'rejectindus')

    return redirect('/ad/industry_list/')
 
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


def get_city_admin(request):
    if request.method == "POST":
        stateinfor = request.POST['stateinfo']
        print("stateinfor :------------------", stateinfor)

        subject = CityMaster.objects.filter(State_Id=stateinfor)
        print("subject------------", subject)

        statewisecity = list(subject.values())
    return JsonResponse({'statewisecity': statewisecity})


def edit_industry(request,id):
    # import pdb;pdb.set_trace()

    ids = request.session['admin_id']
    admin_data = admin.objects.get(id=ids)
    adminname = admin_data.First_name
    edit = Industry_partner.objects.get(id=id)
    uid = edit.id
    Ip = Industry_partner.objects.all()
    state = StateMaster.objects.all()
    city = CityMaster.objects.all()
    if request.method == "GET":
        Ip_Select_Profile = Industry_partner.objects.get(id=edit.id)
        return render(request,"edit_industry.html",{'edit': edit,'Ip_Select_Profile':Ip_Select_Profile,'uid':uid, 'states': state, 'city':city, 'adminname':adminname})
    elif request.method == "POST":
        First_Name = request.POST.get('First_Name')
        Last_name = request.POST.get('Last_name')
        Partner_Type = request.POST.get('Partner_Type')
        Legal_Entity_Name = request.POST.get('Legal_Entity_Name')
        SPOC_Name = request.POST.get('SPOC_Name')
        SPOC_Email = request.POST.get('SPOC_Email')
        Password = request.POST.get('Password')
        SPOC_Phone = request.POST.get('SPOC_Phone')
        Full_Address = request.POST.get('Full_Address')
        State_Name = request.POST.get('State_Name')
        selected_state = StateMaster.objects.get(State_Name=State_Name)
        print('selected_state.id', selected_state.id)
        District_Name = request.POST.get('DistrictName')
        selected_city = CityMaster.objects.get(City_Name=District_Name)
        print('selected_city', selected_city.id)
        PIN_Code = request.POST.get('PIN_Code')
        Office_Phone_No = request.POST.get('Office_Phone_No')
        Website_Link = request.POST.get('Website_Link')
        CreatedDate=datetime.now()
        ModifiedDate=datetime.now()
        Ip = Industry_partner.objects.all()
        user_id = []
        Email_List = []
        for val in Ip:
            user_id.append([val.id,val.SPOC_Email])
            print(val.id, val.SPOC_Email)
        for i in user_id:
            print('i', i)
            if i[0] == edit.id and i[1] == SPOC_Email:
                print('hiii')
            else:
                Email_List.append(str(i[1]))
        Email_one_good = [SPOC_Email]
        if common_data(Email_List, Email_one_good)==True:
            messages.error(request,  'Already Taken, Try with Different Email', extra_tags='admineditverify')
            Ip_Select_Profile = Industry_partner.objects.get(id = edit.id)
            return render(request,"edit_industry.html",{'edit': edit,'Ip_Select_Profile':Ip_Select_Profile,'uid':uid, 'states': state, 'city':city,'adminname':adminname})
        else:
            edit.First_Name = First_Name
            edit.Last_name = Last_name
            edit.Partner_Type = Partner_Type  
            edit.Legal_Entity_Name = Legal_Entity_Name
            edit.SPOC_Name = SPOC_Name
            edit.SPOC_Email = SPOC_Email
            edit.Password = Password
            edit.SPOC_Phone = SPOC_Phone
            edit.Full_Address = Full_Address
            edit.State_Name_id = selected_state.id

            edit.PIN_Code = PIN_Code
            edit.District_Name_id = selected_city.id
            edit.Office_Phone_No = Office_Phone_No
            edit.Website_Link = Website_Link
            edit.CreatedDate = CreatedDate
            edit.ModifiedDate = ModifiedDate
            edit.save()
            messages.error(request,'Industry Edited Successfully', extra_tags = 'indusedit')
        
            return redirect('/ad/industry_list/')
    return render(request, 'edit_industry.html', {'edit': edit, 'adminname': adminname, 'states': state, 'city': city})


def delete_industry(request,id):
   
    dele = Industry_partner.objects.get(id=id)
    print(dele.IsDeleted)
    dele.IsDeleted = 1
    dele.save()
    messages.error(request,'Industry Deleted Successfully', extra_tags = 'indusdelete')
    return redirect('/ad/industry_list/')

# Training Partner

def training_list(request):
    try:
        ids = request.session['admin_id']
        admin_data = admin.objects.get(id=ids)
        adminname = admin_data.First_name
        ids = request.session['admin_id']
        print(ids)
        training = Training_Partner.objects.all().order_by('-id')
        print(training)
        return render(request,'training_list.html', {'training': training, 'adminname': adminname})
    except :
        return redirect('/ad/adlogin/')

def trainingAccept(request, id):
    
    company = Training_Partner.objects.get(id=id)

    mydict={'email':company.Contact_Person_Email, 'regno': company.Password}
    html_template ='admin_mail_Thanks.html'
    html_message = render_to_string(html_template,context=mydict)
    subject="Welcome To Vidhyut Niyojan Applications"
    email_from = EMAIL_HOST_USER

    recipient_list =[company.Contact_Person_Email,company.Password]
    message=EmailMessage(subject,html_message,email_from,recipient_list)
    message.content_subtype ='html'
    message.send()
    company.IsActive = '1'
    company.save()
    messages.error(request,'Training Partner Accepted.', extra_tags = 'trainingaccept')

    return redirect('/ad/training_list/')

def trainingreject(request,id): 
    
    deletecompany = Training_Partner.objects.get(id=id)
    mydict={'email':deletecompany.Contact_Person_Email,'regno':deletecompany.Password}
    html_template ='reject.html'
    html_message = render_to_string(html_template,context=mydict)
    subject="Welcome To Vidhyut Niyojan Applications"
    email_from = EMAIL_HOST_USER

    recipient_list =[deletecompany.Contact_Person_Email]
    message=EmailMessage(subject,html_message,email_from,recipient_list)
    message.content_subtype ='html'
    message.send()
    deletecompany.IsActive = 2
    deletecompany.save()
    messages.error(request,'Training Partner Rejectd.', extra_tags = 'trainingreject')
    
    return redirect('/ad/training_list/')

def add_trainig(request):
    try:
        ids = request.session['admin_id']
        admin_data = admin.objects.get(id=ids)
        adminname = admin_data.First_name
        if request.method == 'POST':
            Nsdc_Registration_Number = request.POST.get('Nsdc_Registration_Number')
            Training_Partner_Name = request.POST.get('Training_Partner_Name')
            Legal_Entity_Name = request.POST.get('Legal_Entity_Name')
            Contact_Person_Name = request.POST.get('Contact_Person_Name')
            Contact_Person_Email = request.POST.get('Contact_Person_Email')
            Contact_Person_Phone = request.POST.get('Contact_Person_Phone')
            Alternate_Email = request.POST.get('Alternate_Email')
            Address = request.POST.get('Address')
            CreatedDate=datetime.now()
            ModifiedDate=datetime.now()
            registerno = random.randint(1000000000, 9999999999)
            loginPassword = request.POST.get('Password')

            if Training_Partner.objects.filter(Contact_Person_Email=Contact_Person_Email).exists():
                messages.error(request, 'ALready exist, Try With Another Email', extra_tags='tev')
                return render(request, 'add_training.html' , {'Nsdc_Registration_Number': Nsdc_Registration_Number, 'Training_Partner_Name': Training_Partner_Name, 'Legal_Entity_Name': Legal_Entity_Name,
                    'Contact_Person_Name': Contact_Person_Name,'Contact_Person_Email':Contact_Person_Email,'Contact_Person_Phone':Contact_Person_Phone, 'Alternate_Email':Alternate_Email, 'Address':Address
                     })
            else:
            
                Industrypartnercreate = Training_Partner( 
                                                        Nsdc_Registration_Number=registerno, 
                                                        Training_Partner_Name = Training_Partner_Name,
                                                        Legal_Entity_Name = Legal_Entity_Name,
                                                        Contact_Person_Name = Contact_Person_Name,
                                                        Contact_Person_Email=Contact_Person_Email,
                                                        Password=loginPassword,
                                                        Contact_Person_Phone =Contact_Person_Phone,
                                                        Alternate_Email=Alternate_Email,
                                                        Address=Address,
                                                        IsDeleted= '0',
                                                        IsActive='1',
                                                        CreatedBy=True,
                                                        CreatedDate=CreatedDate,   
                                                        ModifiedBy=True,
                                                        ModifiedDate=ModifiedDate)
            
                mydict={'email':Contact_Person_Email,'regno':loginPassword}
                html_template ='credential.html'
                html_message = render_to_string(html_template,context=mydict)
                subject="Welcome To Vidhyut Niyojan Applications"
                email_from = EMAIL_HOST_USER

                recipient_list =[Contact_Person_Email,loginPassword]
                message=EmailMessage(subject,html_message,email_from,recipient_list)
                message.content_subtype ='html'
                message.send()
                            
                Industrypartnercreate.save()  
                messages.error(request,'Training Partner Added Successfully', extra_tags = 'Trainingadd')
                print('Industrypartnercreate', Industrypartnercreate)
                return redirect('/ad/training_list/')
        

        return render(request, 'add_training.html', {'adminname':adminname})
    except:
        return redirect('/ad/adlogin/')


def edit_training(request,id):
    # try:
        state = StateMaster.objects.all()
        city = CityMaster.objects.all()
        ids = request.session['admin_id']
        admin_data = admin.objects.get(id=ids)
        adminname = admin_data.First_name
        edit_tr = Training_Partner.objects.get(id=id)
        print(edit_tr.id, 'edit_tredit_tredit_tr')
        uid = edit_tr.id
        Nsdc_Registration_Number = request.POST.get('Nsdc_Registration_Number')
        Training_Partner_Name = request.POST.get('Training_Partner_Name')
        Legal_Entity_Name = request.POST.get('Legal_Entity_Name')
        Contact_Person_Name = request.POST.get('Contact_Person_Name')
        Contact_Person_Email = request.POST.get('Contact_Person_Email')
        Password = request.POST.get('Password')
        Contact_Person_Phone = request.POST.get('Contact_Person_Phone')
        Alternate_Email = request.POST.get('Alternate_Email')
        Address = request.POST.get('Address')

        CreatedDate=datetime.now()
        ModifiedDate=datetime.now()

        if request.method == "GET":
            Ip_Select_Profile = Training_Partner.objects.get(id=edit_tr.id)
            return render(request,"edit_training.html",{'edit_tr': edit_tr,'Ip_Select_Profile':Ip_Select_Profile,'uid':uid, 'states': state, 'city':city})
        elif request.method == "POST":
            Nsdc_Registration_Number = request.POST.get('Nsdc_Registration_Number')
            Training_Partner_Name = request.POST.get('Training_Partner_Name')
            Legal_Entity_Name = request.POST.get('Legal_Entity_Name')
            Contact_Person_Name = request.POST.get('Contact_Person_Name')
            Contact_Person_Email = request.POST.get('Contact_Person_Email')
            Password = request.POST.get('Password')
            Contact_Person_Phone = request.POST.get('Contact_Person_Phone')
            Alternate_Email = request.POST.get('Alternate_Email')
            Address = request.POST.get('Address')
            CreatedDate=datetime.now()
            ModifiedDate=datetime.now()
            Ip = Training_Partner.objects.all()
            user_id = []
            Email_List = []
            for val in Ip:
                user_id.append([val.id,val.Contact_Person_Email])
                print(val.id, val.Contact_Person_Email)
            for i in user_id:
                if i[0] == edit_tr.id and i[1] == Contact_Person_Email:
                    print('hiii')
                else:
                    Email_List.append(str(i[1]))
            Email_one_good = [Contact_Person_Email]
            if common_data(Email_List, Email_one_good)==True:
                messages.error(request,  'Already Taken, Try with Different Email', extra_tags='trainingeditverify')
                Ip_Select_Profile = Training_Partner.objects.get(id = edit_tr.id)
                return render(request,"edit_training.html",{'edit_tr': edit_tr,'Ip_Select_Profile':Ip_Select_Profile,'uid':uid, 'states': state, 'city':city})
            else:
                edit_tr.Nsdc_Registration_Number = Nsdc_Registration_Number
                edit_tr.Training_Partner_Name = Training_Partner_Name
                edit_tr.Legal_Entity_Name = Legal_Entity_Name
                edit_tr.Contact_Person_Name = Contact_Person_Name
                edit_tr.Contact_Person_Email = Contact_Person_Email
                edit_tr.Contact_Person_Phone = Contact_Person_Phone
                edit_tr.Alternate_Email = Alternate_Email
                edit_tr.Password = Password
                edit_tr.Address = Address
                edit_tr.CreatedDate = CreatedDate
                edit_tr.ModifiedDate = ModifiedDate
                edit_tr.save()  
                messages.error(request,'Training Edited Successfully', extra_tags = 'trainingedit')
                return redirect('/ad/training_list/')

        return render(request, 'edit_training.html', {'edit_tr': edit_tr, 'adminname': adminname})
    # except :
    #     return redirect('/ad/adlogin/')

def delete_training(request,id):
    try:
        dele = Training_Partner.objects.get(id=id)
        dele.IsDeleted = 1
        dele.save()
        messages.error(request,'Training Partner Deleted Successfully', extra_tags = 'trainingdelete')
        return redirect('/ad/industry_list/')
    except :
        return redirect('/ad/adlogin/')

# Training Center

def list_center(request):
    try:
        ids = request.session['admin_id']
        admin_data = admin.objects.get(id=ids)
        adminname = admin_data.First_name
        center = Training_center.objects.all().order_by('-id')
        return render(request,'list_center.html', {'center': center, 'adminname': adminname})
    except :
        return redirect('/ad/adlogin/')

def add_training_center(request):
    try:
        ids = request.session['admin_id']
        admin_data = admin.objects.get(id=ids)
        adminname = admin_data.First_name
        industry = Training_Partner.objects.all()
        city = CityMaster.objects.all()
        selectstate = StateMaster.objects.all()
        if request.method == 'POST':
            Training_Partner_Id = request.POST.get('Training_Partner_Id')
            state = request.POST.get('state')
            City = request.POST.get('City')
            Training_Center_Name = request.POST.get('Training_Center_Name')
            Address1 = request.POST.get('Address1')
            Address2 = request.POST.get('Address2')
            Pin_Code = request.POST.get('Pin_Code')
            Contact_Name = request.POST.get('Contact_Name')
            Contact_Email=request.POST.get('Contact_Email')
            Contact_No=request.POST.get('Contact_No')
            registerno = random.randint(1000000000, 9999999999)
            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
            
            Industrypartnercreate = Training_center(registerno=registerno,
                                                    Training_Partner_Id_id=Training_Partner_Id, 
                                                    state_id = state,
                                                    City_id = City,
                                                    Training_Center_Name = Training_Center_Name,
                                                    Address1=Address1,
                                                    Address2=Address2,
                                                    Pin_Code=Pin_Code,
                                                    Contact_Name=Contact_Name,
                                                    Contact_Email=Contact_Email,
                                                    Password=loginPassword, 
                                                    Contact_No=Contact_No,
                                                    IsDeleted= '0',
                                                    IsActive='1',
                                                    )


            mydict={'email':Contact_Email,'regno':loginPassword}
            html_template ='credential.html'
            html_message = render_to_string(html_template,context=mydict)
            subject="Welcome To Vidhyut Niyojan Applications"
            email_from = EMAIL_HOST_USER

            recipient_list =[Contact_Email,loginPassword]
            message=EmailMessage(subject,html_message,email_from,recipient_list)
            message.content_subtype ='html'
            message.send()
                        
                        
            Industrypartnercreate.save()  
            messages.error(request,'Training Center Added Successfully', extra_tags = 'centeradd')
            print('Industrypartnercreate', Industrypartnercreate)
            return redirect('/ad/list_center/')
        return render(request, 'admin_add_center.html', {'industry': industry,'selectstate': selectstate, 'city': city , 'adminname' :adminname})
    except :
        return redirect('/ad/adlogin/')

def centerAccept(request, id):
    
    company = Training_center.objects.get(id=id)

    mydict={'email':company.Contact_Email,'regno':company.Password}
    html_template ='admin_mail_thanks.html'
    html_message = render_to_string(html_template,context=mydict)
    subject="Welcome To Vidhyut Niyojan Applications"
    email_from = EMAIL_HOST_USER

    recipient_list =[company.Contact_Email,company.Password]
    message=EmailMessage(subject,html_message,email_from,recipient_list)
    message.content_subtype ='html'
    message.send()
    company.IsActive = '1'
    company.save()
    messages.error(request,'Training Center Accepted.', extra_tags = 'centeraccepted')

    return redirect('/ad/list_center/')

def centerReject(request,id): 
    
    deletecompany = Training_center.objects.get(id=id)
    mydict={'email':deletecompany.Contact_Email,'regno':deletecompany.Password}
    html_template ='reject.html'
    html_message = render_to_string(html_template,context=mydict)
    subject="Welcome To Vidhyut Niyojan Applications"
    email_from = EMAIL_HOST_USER

    recipient_list =[deletecompany.Contact_Email]
    message=EmailMessage(subject,html_message,email_from,recipient_list)
    message.content_subtype ='html'
    message.send()
    deletecompany.IsActive = 2
    deletecompany.save()
    messages.error(request,'Training Center Rejected.', extra_tags = 'centerrejected')

    return redirect('/ad/list_center/')

def edit_center(request,id):
    try:
        ids = request.session['admin_id']
        admin_data = admin.objects.get(id=ids)
        adminname = admin_data.First_name
        industry = Training_Partner.objects.all()
        city = CityMaster.objects.all()
        selectstate = StateMaster.objects.all()
        edit_cen = Training_center.objects.get(id=id)
        Training_Partner_Id = request.POST.get('Training_Partner_Id')
        state = request.POST.get('state')
        City = request.POST.get('City')
        Training_Center_Name = request.POST.get('Training_Center_Name')
        Address1 = request.POST.get('Address1')
        Address2 = request.POST.get('Address2')
        Pin_Code = request.POST.get('Pin_Code')
        Contact_Name = request.POST.get('Contact_Name')
        Contact_Email = request.POST.get('Contact_Email')
        Contact_No = request.POST.get('Contact_No')

        if request.method == 'POST':
            edit_cen.Training_Partner_Id_id  = Training_Partner_Id
            edit_cen.state_id = state
            edit_cen.City_id = City
            edit_cen.Training_Center_Name = Training_Center_Name
            edit_cen.Address1 = Address1
            edit_cen.Address2 = Address2
            edit_cen.Pin_Code = Pin_Code
            edit_cen.Contact_Name = Contact_Name
            edit_cen.Contact_Email = Contact_Email
            edit_cen.Contact_No = Contact_No
            edit_cen.save()  
            messages.error(request,'Training Center Edited Successfully', extra_tags = 'edited')
            return redirect('/ad/list_center/')
        else:
            messages.error(request, 'Edit is not work')
            

        return render(request, 'edit_center.html', {'edit_cen': edit_cen, 'selectstate': selectstate, 'city':city, 'industry':industry, 'adminname':adminname})
    except:
        return redirect('/ad/adlogin/')

def delete_center(request,id):
    dele = Training_center.objects.get(id=id)
    dele.IsDeleted = 1
    dele.save()
    messages.error(request,'Training Center Deleted Successfully', extra_tags = 'jobpostdeleted')
    return redirect('/ad/list_center/')

def setting(request):
    return render(request, 'setting.html')

def admin_rpl_list(request):
    ids = request.session['admin_id']
    admin_data = admin.objects.get(id=ids)
    adminname = admin_data.First_name
    list_of_rpl = RPL_Master.objects.filter(Is_deleted=0)
    print(list_of_rpl)
    return render(request, 'admin_rpl_list.html', {'list_of_rpl': list_of_rpl,'adminname':adminname})

def rpl_deleted(request,id):
    rpl_delete = RPL_Master.objects.get(id=id)
    rpl_delete.Is_deleted = 1
    rpl_delete.save()
    messages.error(request,'RPL Deleted Successfully', extra_tags = 'rpldeleted')
    return redirect('/ad/admin_rpl_list/')

def add_job(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        opening_for = request.POST.get('opening_for')
        reqiured_Skill = request.POST.get('reqiured_Skill')
        location = request.POST.get('location')
        job_cureentdate = request.POST.get('job_cureentdate')
    else:
        Jobfaircreate = Job_fair(job_title=First_Name,
                                 job_description=Last_name,
                                 opening_for=Partner_Type,
                                 reqiured_Skill=Legal_Entity_Name,
                                 location=SPOC_Name,
                                 job_cureentdate=SPOC_Email,
                                 IsDeleted='0',
                                 IsActive='1',

                                 )
        Jobfaircreate.save()
    return redirect('/ad/jobfair_list/')


def jobfairlist(request):
    jobfair = Job_fair.objects.all()
    return render(request, 'jobfair_list.html')


def edit_jobfair(request, id):
    edit_job = Job_fair.objects.get(id=id)
    if request.method == "GET":
        job_Select_Profile = Job_fair.objects.get(id=edit_job.id)
        return render(request, "jobfair_edit.html", {'edit_job': edit_job, 'job_Select_Profile': job_Select_Profile})
    elif request.method == "POST":
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        opening_for = request.POST.get('opening_for')
        reqiured_Skill = request.POST.get('reqiured_Skill')
        location = request.POST.get('location')
        job_cureentdate = request.POST.get('job_cureentdate')
    else:   
            edit_job.job_title = job_title
            edit_job.job_description = job_description
            edit_job.opening_for = opening_for
            edit_job.reqiured_Skill = reqiured_Skill
            edit_job.location = location
            edit_job.job_cureentdate = job_cureentdate

            edit_job.save()

            return redirect('/ad/jobfairlist/')


    return render(request, 'jobfair_edit.html', {'edit_job': edit_job}).save()
    messages.error(request, 'JOb Fair Edited Successfully', extra_tags='jobfairedit')

    return redirect('/ad/jobfairlist/')
    return render(request, 'jobfair_edit.html', {'edit_job': edit_job})


def delete_jobfair(request, id):
    dele = Job_fair.objects.get(id=id)
    dele.IsDeleted = 1
    dele.save()
    messages.error(request, 'Job Fair Deleted Successfully', extra_tags='jobfairdelete')
    return redirect('/ad/jobfairlist/')



