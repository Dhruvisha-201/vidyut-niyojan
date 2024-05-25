from django.shortcuts import render, redirect
import os
# Create your views here.
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.conf import settings
from .models import *
from IndustryPartner.models import *
from django.contrib import messages
import string
from .function import handle_uploaded_file
from vidhyut_niyojan.settings import EMAIL_HOST_USER
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string, get_template
from django.template import Context, Template, RequestContext
from django.core.mail import EmailMessage
import random
from vidhyut_niyojan.settings import BASE_DIR
import csv
from .form import CandidateMasterForm
# from django.shortcuts import render
import re
from datetime import date

# Create your views here.
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse

def training_register(request):
    if request.method == "POST":
        nsdc_r_number=request.POST.get('Nsdc_Registration_Number')
        t_pname = request.POST.get('Training_Partner_Name')
        l_ename = request.POST.get('Legal_Entity_Name')
        c_pname = request.POST.get('Contact_Person_Name')
        c_pemail = request.POST.get('Contact_Person_Email')

        c_phone = request.POST.get('Contact_Person_Phone')
        a_email = request.POST.get('Alternate_Email')
        address = request.POST.get('Address')
        CreatedDate = datetime.today()
        ModifiedDate = datetime.today()
        characters = string.ascii_letters + string.digits
        Password = request.POST.get('Password')
        Confirm_pass = request.POST.get('Confirm_pass')
        print("password : ---------------------", Password)
        print("Confirm_pass : ---------------------", Confirm_pass)
        reg = r'\b^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$\b'
        if(re.fullmatch(reg, Password)):
            if Password == Confirm_pass:
                pass
            else:
                messages.error(request,'New Password And Confirm Password Does Not Match', extra_tags = 'navopassword')
                return render(request,"trainingpartner_signup.html",{"t_pname":t_pname,"l_ename":l_ename,"c_pname":c_pname,"c_pemail":c_pemail,"c_phone":c_phone,
                "a_email":a_email, 'address':address, 'nsdc_r_number':nsdc_r_number})
        else:
            messages.error(request,'Your password is weak, Please including Uppercase, Lowercase, Numbers and Special character', extra_tags = 'pwn')
            return render(request,"trainingpartner_signup.html",{"t_pname":t_pname,"l_ename":l_ename,"c_pname":c_pname,"c_pemail":c_pemail,"c_phone":c_phone,
            "a_email":a_email, 'address':address, 'nsdc_r_number':nsdc_r_number})

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, c_pemail)):
            pass
        else:
            print("invalid email")
            e_msg = "PLEASE ENTER VALID EMAIL"
            return render(request, "trainingpartner_signup.html", {'e_msg': e_msg})
        
        if Industry_partner.objects.filter(SPOC_Phone=c_phone).exists() or Training_Partner.objects.filter(Contact_Person_Phone=c_phone).exists():
            messages.error(request, "Phone Number is Already Taken, Try With Another Number", extra_tags="phoneverify")
            return render(request,"trainingpartner_signup.html",{"t_pname":t_pname,"l_ename":l_ename,"c_pname":c_pname,"c_pemail":c_pemail,"c_phone":c_phone,
            "a_email":a_email, 'address':address, 'nsdc_r_number':nsdc_r_number})
        
        elif Industry_partner.objects.filter(SPOC_Email=c_pemail).exists() or Training_Partner.objects.filter(Contact_Person_Email=c_pemail).exists():
            messages.error(request, "Email is Already Taken, Try With Another", extra_tags="emailverify")
            return render(request,"trainingpartner_signup.html",{"t_pname":t_pname,"l_ename":l_ename,"c_pname":c_pname,"c_pemail":c_pemail,"c_phone":c_phone,
            "a_email":a_email, 'address':address, 'nsdc_r_number':nsdc_r_number})
        

        else:

            trainingpartner = Training_Partner(Nsdc_Registration_Number=nsdc_r_number,
                                            Training_Partner_Name=t_pname,
                                            Legal_Entity_Name=l_ename,
                                            Contact_Person_Name=c_pname,
                                            Contact_Person_Email=c_pemail,
                                            Password=Password,
                                            Contact_Person_Phone=c_phone,
                                            Alternate_Email=a_email,
                                            Address=address,
                                            IsDeleted='0',
                                            IsActive='0',
                                            CreatedBy='raj',
                                            CreatedDate=CreatedDate,
                                            ModifiedBy='raj',
                                            ModifiedDate=ModifiedDate
                                            )

            mydict = {'email': c_pemail, 'regno': nsdc_r_number}
            html_template = 'tp_register_email.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = "Welcome To vidhyut_niyojan Applications"
            email_from = EMAIL_HOST_USER

            recipient_list = [c_pemail, nsdc_r_number]
            message = EmailMessage(subject, html_message, email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()

            trainingpartner.save()
            return redirect('/Tp/thank/')

    else:
        return render(request, 'trainingpartner_signup.html')

def training_logout(request):
    if 'training_id' in request.session:
        # logout(request)
        return redirect('/Tp/training_login/')
    else:
        return render(request, 'training_Login.html')

def training_login(request):
    if request.method == "POST":
        email = request.POST.get('Contact_Person_Email')
        print("Contact_Person_Email : ------------", email)
        passw = request.POST.get('Password')
        print("passw : ------------", passw)
        try:
            uid = Training_Partner.objects.get(Contact_Person_Email=email)
            print("uid : ------------", uid)

            if email == uid.Contact_Person_Email:
                if passw == uid.Password:
                    request.session['training_id'] = uid.id
                    request.session['Contact_Person_Email'] = uid.Contact_Person_Email
                    messages.error(request, "Successfully Login...!", extra_tags='loginadded')
                    return redirect('/Tp/training_dashboard/')

                else:
                    messages.error(request, 'Invalid Credential', extra_tags='tlog')
                    return render(request, 'training_Login.html')
            else:
                messages.error(request, 'Invalid Credential', extra_tags='tlog')
                return render(request, 'training_Login.html')
        except :
            messages.error(request, 'Invalid Credential', extra_tags='tlog')
            return render(request, 'training_Login.html')
    else:
        pass

    return render(request, "training_Login.html")

def training_dashboard(request):
    # try:
    user = request.session['training_id']
    uid = Training_Partner.objects.get(id=user)
    TC = Training_center.objects.filter(Training_Partner_Id=uid).count()
    NC = CandidateMaster.objects.filter(Training_Partner_Id=uid).count()
    candidatelist = CandidateMaster.objects.filter(Training_Partner_Id=uid)
    print("candidatellist : ---------------------",candidatelist)
    return render(request, 'training_index.html', {'uid': uid, 'TC': TC, 'NC': NC,'candidatelist':candidatelist})
    # except:
    #     messages.error(request, 'you have to login first')
    #     return redirect('/Tp/training_login/')


def get_reg_number(request):
    if request.method == 'POST':
        regno = request.POST.get('registernumber')

        all_training_reg = Training_Partner.objects.all()
        for x in all_training_reg:
            if x.Nsdc_Registration_Number == regno:
                registermo = Training_Partner.objects.get(Nsdc_Registration_Number=regno)
                print('registermo', registermo.IsActive)

                return render(request, 'current_reg_status.html', {'registermo': registermo})
        else:
            print("hjsdghsgfhsdgfhdsj")
            messages.error(request, 'Please Enter Valid Register Number', extra_tags='traininreg')
            return render(request, 'current_reg_status.html')
    else:
        return render(request, 'current_reg_status.html')

        # return render(request,'current_reg_status.html')

def center_list(request):
    try:
        user = request.session['training_id']
        uid = Training_Partner.objects.get(id=user)
        partner_center_list = Training_center.objects.filter(Training_Partner_Id=user, IsDeleted=0).order_by('-id')
        print('partner_center_list', partner_center_list)

        center = Training_center.objects.filter(IsDeleted=0)
        return render(request, 'training_center_list.html', {'center': center, 'uid': uid, 'partner_center_list':partner_center_list})
    except:
        messages.error(request, 'you have to login first')
        return render(request, 'training_Login.html')

    


def add_training_center(request):
    try:
        user = request.session['training_id']
        uid = Training_Partner.objects.get(id=user)

        Training = Training_Partner.objects.all()
        city = CityMaster.objects.all()
        selectstate = StateMaster.objects.all()
        if request.method == 'POST':
            Training_Partner_Id = request.session['training_id']
            state = request.POST.get('state')
            print("state: ", state)
            City = request.POST.get('city')
            print("city: ", City)

            selected_state = StateMaster.objects.get(id=state)
            selected_city = CityMaster.objects.get(City_Name=City)
            print("selected city:   ", selected_city)
            selcity = CityMaster.objects.get(id=selected_city.id)
            print("selcity :- ----------", selcity)

            Training_Center_Name = request.POST.get('Training_Center_Name')
            Address1 = request.POST.get('Address1')
            Address2 = request.POST.get('Address2')
            Pin_Code = request.POST.get('Pin_Code')
            print("pincode: -------------------", Pin_Code)
            Contact_Name = request.POST.get('Contact_Name')
            Contact_Email = request.POST.get('Contact_Email')

            CreatedDate = datetime.today()
            ModifiedDate = datetime.today()

            regex = r'\b[a-z0-9._%+-]+@+[a-z]+.com\b'
            if (re.fullmatch(regex, Contact_Email)):
                pass
            else:
                print("invalid email")
                e_msg = "PLEASE ENTER VALID EMAIL"
                return render(request, "add_center.html", {'e_msg': e_msg})

            Contact_No = request.POST.get('Contact_No')
            registerno = random.randint(1000000000, 9999999999)
            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            # for x in selected_city:
            Trainingpartnercreate = Training_center(registerno=registerno,
                                                    Training_Partner_Id_id=Training_Partner_Id,
                                                    state=selected_state,
                                                    City=selcity,
                                                    Training_Center_Name=Training_Center_Name,
                                                    Address1=Address1,
                                                    Address2=Address2,
                                                    Pin_Code=Pin_Code,
                                                    Contact_Name=Contact_Name,
                                                    Contact_Email=Contact_Email,
                                                    Password=loginPassword,
                                                    Contact_No=Contact_No,
                                                    IsDeleted='0',
                                                    IsActive='0',
                                                    CreatedBy='bansri',
                                                    CreatedDate=CreatedDate,
                                                    ModifiedBy='bansri',
                                                    ModifiedDate=ModifiedDate,
                                                    )
            

            mydict = {'email': Contact_Email, 'regno': registerno}
            html_template = 'tp_register_email.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = "Welcome To vidhyut_niyojan Applications"
            email_from = EMAIL_HOST_USER

            recipient_list = [Contact_Email, registerno]
            message = EmailMessage(subject, html_message, email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()

            Trainingpartnercreate.save()
            print('Trainingpartnercreate', Trainingpartnercreate)
            return redirect('/Tp/center_list/')
    

        return render(request, 'add_center.html',
                  {'Training': Training, 'selectstate': selectstate, 'city': city, 'uid': uid})
    except:
        messages.error(request,'you have to login first')
        return redirect('/Tp/training_login/')


def thank(request):
    return render(request,'thanku.html')

def get_city_ajax(request):
    if request.method == "POST":
        stateinfor = request.POST['stateinfo']
        print("stateinfor :------------------", stateinfor)

        subject = CityMaster.objects.filter(State_Id=stateinfor)
        print("subject------------", subject)

        statewisecity = list(subject.values())
    return JsonResponse({'statewisecity': statewisecity})


def edit_center(request, id):
    try:
        user = request.session['training_id']
        uid = Training_Partner.objects.get(id=user)

        if request.method == "GET":

            city = CityMaster.objects.all()
            state = StateMaster.objects.all()
            edit_cen = Training_center.objects.get(id=id)

            return render(request, 'training_center_edit.html',
                        {'edit_cen': edit_cen, 'city': city, 'state': state, 'uid': uid})

        elif request.method == 'POST':
            city = CityMaster.objects.all()
            state = StateMaster.objects.all()
            edit_cen = Training_center.objects.get(id=id)

            Citis = request.POST.get('City')
            states = request.POST.get('state')
            train_cen = request.POST.get('center_name')
            Address1 = request.POST.get('Address1')
            Address2 = request.POST.get('Address2')
            Pin_Code = request.POST.get('Pin_Code')
            Contact_Name = request.POST.get('Contact_Name')
            ContactEmail = request.POST.get('Contact_Email')
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if (re.fullmatch(regex, ContactEmail)):
                pass
            else:
                print("invalid email")
                messages.error(request, 'please enter valid email', extra_tags='trainingcenemail')
                return render(request, "training_center_edit.html",
                            {'edit_cen': edit_cen, 'city': city, 'state': state, 'uid': uid})

            Contact_No = request.POST.get('Contact_No')

            state_id = StateMaster.objects.get(id=states)
            city_id = CityMaster.objects.get(id=Citis)

            edit_cen.City = city_id
            edit_cen.state = state_id
            edit_cen.Training_Center_Name = train_cen
            edit_cen.Address1 = Address1
            edit_cen.Address2 = Address2
            edit_cen.Pin_Code = Pin_Code
            edit_cen.Contact_Name = Contact_Name
            edit_cen.Contact_Email = ContactEmail
            edit_cen.Contact_No = Contact_No
            edit_cen.save()
            messages.error(request, 'Save Changes', extra_tags='updatedcenter')
            return redirect('/Tp/center_list/')
            
    except:
        messages.error(request,'you have to login first')
        return redirect('/Tp/training_login/')


def delete_center(request, id):
    dele = Training_center.objects.get(id=id)
    dele.IsDeleted = 1
    dele.save()
    messages.error(request, "Training Centerd Deleted Successfully", extra_tags="cen_delete")
    return redirect('/Tp/center_list/')

def add_candidate(request):
    if request.method == "GET":
        user = request.session['training_id']
        uid = Training_Partner.objects.get(id=user)
        # candidte = CandidtaeMaster.objects.all()
        city = CityMaster.objects.all()
        selectstate = StateMaster.objects.all()
        selectcourse = CourceMaster.objects.all()
        selecttrainingcenter = Training_center.objects.all()

        return render(request, 'add_candidate.html',
                      {'selectstate': selectstate, 'selectcourse': selectcourse, 'city': city,
                       'selecttrainingcenter': selecttrainingcenter, 'uid': uid})

    elif request.method == 'POST':
        city = CityMaster.objects.all()
        selectstate = StateMaster.objects.all()
        selectcourse = CourceMaster.objects.all()
        selecttrainingcenter = Training_center.objects.all()
        Training_partner_Id = request.session['training_id']
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(8))
        training_id = Training_Partner.objects.get(id=Training_partner_Id)
        selectedstate = request.POST.get('state')
        state = StateMaster.objects.get(id=selectedstate)
        center_id = request.POST.get('Center_Id')
        print('center_id', center_id)
        training_C_id = Training_center.objects.get(id=center_id)
        selectedCity = request.POST.get('city')
        print(selectedCity)

        # City = CityMaster.objects.get(City_Name=selectedCity)
        selectedcourse = request.POST.get('course')
        course = CourceMaster.objects.get(id=selectedcourse)
        fname = request.POST.get('FirstName')
        lname = request.POST.get('LastName')
        gender = request.POST.get('gender')
        cemail = request.POST.get('Candidate_Email')
        phone_no = request.POST.get('Phone_no')
        address1 = request.POST.get('Address1')
        address2 = request.POST.get('Address2')
        pincode = request.POST.get('pincode')
        qualification = request.POST.get('Qualification')
        dob = request.POST.get('DOB')
        adhar_no = request.POST.get('Adhar_Number')
        willingtorelocated = request.POST.get('willing_to_relocate')
        diffrentlyable = request.POST.get('differently_abled')
        jobrole = request.POST.get('Job_role')
        trainingtype = request.POST.get('Training_Type')
        trainigstatus = request.POST.get('Training_Status')
        placedstatus = request.POST.get('Placed_Status')
        disability = request.POST.get('disability')
        tschemename = request.POST.get('Training_Scheme_Name')

        otp = random.randint(10000, 99999)
        otpisused = '0'
        CreatedDate = datetime.today()
        ModifiedDate = datetime.today()
        regex = r'\b[a-z0-9._%+-]+@+[a-z]+.com\b'
        if (re.fullmatch(regex, cemail)):
            pass
        else:
            print("invalid email")
            e_msg = "PLEASE ENTER VALID EMAIL"
            return render(request, "add_candidate.html", {'e_msg': e_msg})
        
        if CandidateMaster.objects.filter(Candidate_Email=cemail).exists():
            messages.error(request, 'Email is already Taken, Try With Another', extra_tags='can_email_verify')
            return render(request,'add_candidate.html', {'fname': fname, 'lname': lname, 'gender': gender,'cemail':cemail, 'phone_no':phone_no, 'address1':address1, 
                                                        'address2' :address2 , 'pincode': pincode, 'qualification': qualification, 'dob': dob, 'adhar_no':adhar_no,
                                                         'willingtorelocated':willingtorelocated, 'diffrentlyable': diffrentlyable,
                                                        'jobrole': jobrole, 'trainingtype': trainingtype, 'trainigstatus': trainigstatus, 'placedstatus': placedstatus,
                                                        'disability': disability, 'tschemename': tschemename, 'city': city,
                                                         'selectstate': selectstate, 'selectcourse': selectcourse , 'selecttrainingcenter': selecttrainingcenter })
        else:
            CandidtaeMastersave = CandidateMaster(Training_Partner_Id_id=request.session['training_id'],
                                                Training_Center_Id_id=center_id,
                                                State_Id=state,
                                                City_Id_id=selectedCity,
                                                Course_Id=course,
                                                FirstName=fname,
                                                LastName=lname,
                                                Gender=gender,
                                                Candidate_Email=cemail,
                                                Candidate_password=password,
                                                Phone_no=phone_no,
                                                Address1=address1,
                                                Address2=address2,
                                                pincode=pincode,
                                                Qualification=qualification,
                                                DOB=dob,
                                                adhar_Number=adhar_no,
                                    
                                                willing_to_relocate=willingtorelocated,
                                                differently_abled=diffrentlyable,
                                                Job_role=jobrole,
                                                Training_Type=trainingtype,
                                                Training_Status=trainigstatus,
                                                Placed_Status=placedstatus,
                                                Training_Scheme_Name=tschemename,
                                                otp=otp,
                                                otp_is_used='0',
                                                IsDeleted='0',
                                                IsActive='0',
                                                CreatedBy='bansri',
                                                CreatedDate=CreatedDate,
                                                ModifiedBy='bansri',
                                                ModifiedDate=ModifiedDate,


                                                )

            mydict = {'email': cemail, 'regno': password, 'otp': otp}
            html_template = 'candidate_credential.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = "Welcome To Vidhyut Niyojan Applications"
            email_from = EMAIL_HOST_USER

            recipient_list = [cemail, password]
            message = EmailMessage(subject, html_message, email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            # import pdb;pdb.set_trace()
            CandidtaeMastersave.save()

            messages.error(request,"Candidate Added successfully",extra_tags='cadidadd')
            return redirect('/Tp/candidate_list/')


def loginverify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print('email-------------------------->', email)
        ottp = request.POST.get('otp')
        print('ottp--------------------------->', ottp)
        if CandidateMaster.objects.filter(Candidate_Email=email):
            request.session['candidate_Email'] = email
            if CandidateMaster.objects.filter(otp=ottp):

                return redirect('/cm/candidate_dashboard/')
            else:
                print('otp not matched')
                messages.error(request, 'OTP Not Matched',  extra_tags='otpnm')
        else:
            print('emial not matched')
            messages.error(request, 'Email is Not Matched.', extra_tags='enm')
    return render(request, 'loginverify.html')


def candidate_list(request):
    try:
        user = request.session['training_id']
        print(user)
        uid = Training_Partner.objects.get(id=user)

        t_c = Training_center.objects.filter(Training_Partner_Id=user)
        print('t_c', t_c)


        partner_center_list = CandidateMaster.objects.filter(Training_Partner_Id=user ,IsDeleted=0)
 
        print(partner_center_list)


        return render(request, 'candidate_list.html', {'uid': uid, 'partner_center_list': partner_center_list})

    except:
        messages.error(request, 'you have to login first')
        return redirect('/Tp/training_login/')


def edit(request, id):
    employee = CandidateMaster.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})


def edit_candidate(request, id):

    user = request.session['training_id']
  
    uid = Training_Partner.objects.get(id=user)

    TP = Training_Partner.objects.all()

    
    obj = get_object_or_404(CandidateMaster, id=id)
    get_qu = CandidateMaster.objects.get(id=id)
    form = CandidateMasterForm(request.POST or None, instance=obj)
    qualification =request.POST.get('Qualification') 
   
    if form.is_valid():
        obj = form.save(commit=False)
        obj.Qualification = qualification
        obj.save()
        messages.error(request, 'Save Changes', extra_tags='cadidupdate')

        return HttpResponseRedirect("/Tp/candidate_list/")



    return render(request, "candidate_edit.html", {'form': form, 'get_qu': get_qu , 'obj': obj, 'uid': uid, 'TP': TP})

def delete_candidate(request, id):
    dele = CandidateMaster.objects.get(id=id)
    dele.IsDeleted = 1
    dele.save()
    messages.error(request, "Candidate Deleted Successfully", extra_tags="candiddelete")
    # messages.error(request, "Candidate Deleted Successfully", extra_tags="candiddelete")
    return redirect('/Tp/candidate_list/')


def training_setting(request):
    try:
        user = request.session['training_id']
        uid = Training_Partner.objects.get(id=user)
    except:
        messages.error(request, 'you have to login first')
    return render(request, 'Training_setting.html', {'uid': uid})


def trainig_contact_us(request):
    try:
        user = request.session['training_id']
        uid = Training_Partner.objects.get(id=user)
    except:
        messages.error(request, 'you have to login first')
    return render(request, 'training_contactus.html', {'uid': uid})


def TP_profile(request):
    try:
        user = request.session['training_id']
        uid = Training_Partner.objects.get(id=user)
        TP_View_Profile = Training_Partner.objects.get(id=request.session['training_id'])
        print("TP_View_Profile", TP_View_Profile)
        return render(request, "TP_profile.html", {'TP_View_Profile': TP_View_Profile, 'uid': uid})

    except:
        messages.error(request, 'you have to login first')
        return redirect('/Tp/training_login/')

    
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

def TP_Update_Profile(request):
    user = request.session['training_id']
    uid = Training_Partner.objects.get(id=user)
    if request.method == "GET":
        TP_select_Profile = Training_Partner.objects.get(id=request.session['training_id'])
        return render(request, "edit_TP_profile.html", {'TP_select_Profile': TP_select_Profile, 'uid': uid})
    elif request.method == "POST":
        TP_Name = request.POST.get('Training_Partner_Name')
        print("TP_Name : -============-------------", TP_Name)
        nsdc_number = request.POST.get('Nsdc_Registration_Number')
        print("nsdc_number : -============-------------", nsdc_number)
        TP_Legal_Entity_Name = request.POST.get('Legal_Entity_Name')
        print("TP_Legal_Entity_Name : -============-------------", TP_Legal_Entity_Name)
        TP_Contact_Person_Name = request.POST.get('Contact_Person_Name')
        print("TP_Contact_Person_Name : -============-------------", TP_Contact_Person_Name)
        TP_Contact_Person_Email = request.POST.get('Contact_Person_Email')
        print("TP_Contact_Person_Email : -============-------------", TP_Contact_Person_Email)
        TP_Contact_Person_Phone = request.POST.get('Contact_Person_Phone')
        print("TP_Contact_Person_Phone : -============-------------", TP_Contact_Person_Phone)
        TP_Alternate_Email = request.POST.get('Alternate_Email')
        print("TP_Alternate_Email : -============-------------", TP_Alternate_Email)
        TP_Address = request.POST.get('Address')
        print("TP_Address : -============-------------", TP_Address)
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, TP_Contact_Person_Email)):
            pass
        else:
            print("invalid email")
            TP_select_Profile = Training_Partner.objects.get(id=request.session['training_id'])
            messages.error(request, 'PLEASE ENTER VALID EMAIL', extra_tags='e_msg')
            return render(request, "edit_TP_profile.html", {'uid': uid,'TP_select_Profile':TP_select_Profile})

        Ip = Training_Partner.objects.all()
        user_id = []
        Email_List = []
        print('user----------------------', request.session['training_id'])
        for val in Ip:
            user_id.append([val.id,val.Contact_Person_Email])
            print(val.id, val.Contact_Person_Email)
        print(user_id,"EWRWE")
        for i in user_id:
            if i[0] == request.session['training_id'] and i[1] == TP_Contact_Person_Email:
                print('hiii')
            else:
                Email_List.append(str(i[1]))
        print(Email_List,'-----------------------')
        
        Email_one_good = [TP_Contact_Person_Email]
        if common_data(Email_List, Email_one_good)==True:
            messages.error(request,  'Already Taken, Try with Different Email', extra_tags='editverify')
            Ip_Select_Profile = Training_Partner.objects.get(id = request.session['training_id'])
            return render(request,"edit_TP_profile.html",{'TP_select_Profile':Ip_Select_Profile,'uid':uid, 'state': state})
        else:
            TP_select_Profile = Training_Partner.objects.get(id=request.session['training_id'])
            
            TP_select_Profile.Nsdc_Registration_Number = nsdc_number
            TP_select_Profile.Training_Partner_Name = TP_Name
            TP_select_Profile.Legal_Entity_Name = TP_Legal_Entity_Name
            TP_select_Profile.Contact_Person_Name = TP_Contact_Person_Name
            TP_select_Profile.Contact_Person_Email = TP_Contact_Person_Email
            request.session['Contact_Person_Email'] = TP_Contact_Person_Email
            TP_select_Profile.Contact_Person_Phone = TP_Contact_Person_Phone
            TP_select_Profile.Alternate_Email = TP_Alternate_Email
            TP_select_Profile.Address = TP_Address
            TP_select_Profile.save()
            return redirect('/Tp/TP_profile/')
        
def change_passwor(request):
    user = request.session['Contact_Person_Email']
    print(user)
    uid = Training_Partner.objects.get(Contact_Person_Email=user)
    if request.method == "POST":
        old_password=request.POST.get('oldpass')
        newpassw=request.POST.get('newpassword')
        confirmpassw=request.POST.get('confirmpassword')
    
        if uid.Password == old_password:
            regex = r'\b^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$\b'
            if(re.fullmatch(regex, newpassw)):
                if newpassw == confirmpassw:
                    uid.Password = newpassw
                    uid.save()
                    return redirect('/Tp/TP_profile/')
                else:
                    messages.error(request,'New Password And Confirm Password Does Not Match', extra_tags = 'navopassword')
                return render(request,"TP_change_password.html",{'uid':uid})   
            else:
                messages.error(request,'Your password is weak, Please including Uppercase, Lowercase, Numbers and Special character', extra_tags = 'pwn')
                return render(request,"TP_change_password.html",{'uid':uid})
        else:
            messages.error(request,'Please Enter Valid Old Password', extra_tags = 'oldpas')
            return render(request,"TP_change_password.html", {'uid': uid})
    else:
        return render(request,"TP_change_password.html", {'uid': uid})


now = datetime.now()
city = '0'
state = '0'
def bulkupload(request):
    center_id_get = request.POST.get('Training_Center_Id')
    # import pdb;pdb.set_trace()
    user = request.session['training_id']
    print('user', user)
    uid = Training_Partner.objects.get(id=user)
    get_center = Training_center.objects.filter(Training_Partner_Id=user)
    data = bulk_upload.objects.filter(Training_Partner_Id=user)
    candidate_name = Training_Partner.objects.get(id=request.session['training_id'])
    states = CityMaster.objects.all()
    if request.method == 'POST':
        my_files = request.FILES['bulk_upload_file']
        handle_uploaded_file(my_files)
        total = os.path.join(BASE_DIR) + '/TrainingPartner/static/csv/' + str(my_files)
        total_row_count = 0
        candidtae_data = []
        filterdata = []

        with open(total) as f:
            files = csv.reader(f)
            lines = len(list(files))
        print('lines', lines)
        with open(total) as f:
            files = csv.reader(f)
            for val in files:
                candidtae_data.append(val)
            for items in candidtae_data[1:]:
                if items[0] == '' or items[1] == '' or items[2] == '' or items[3] == '' or items[4] == '' or \
                        items[5] == '' or items[6] == '' or items[7] == '' or items[8] == '':
                    li = len(items)
                    # print('li', li)
                else:
                    filterdata.append(items)
                    for item in filterdata:
                        if request.method == 'POST':
                            center_id_get = request.POST.get('Training_Center_Id')
                            FirstName = item[0]
                            LastName = item[1]
                            Candidate_Email = item[3]
                            dob = '2022-01-01'
                            Phone_no = item[4]
                            adhar_number = item[5]
                            adhar_enroll_number = item[6]
                            Gender = item[7]
                            willing_to_relocate = item[8] 
                            differently_abled = item[9]
                            state = item[10]
                            city = item[11]
                            Address1 = item[12]
                            job_role=item[13]
                            training_type=item[14]
                            training_center_detail = item[15]
                            training_status = item[16]
                            placed_status = item[17]
                            disability = item[18]
                            training_scheme_name = item[19]
                            pincode = item[7]
                            Qualification = item[20]
                            print(FirstName, LastName, Candidate_Email, dob, Phone_no, adhar_number,adhar_enroll_number, Gender, 
                            willing_to_relocate, differently_abled, state, city, Address1, job_role, training_status, placed_status, disability, training_scheme_name)
                            print('city',item[10])
                            for new_city in states:
                                if  (item[10]).lower() in (new_city.City_Name).lower() :
                                    city =  new_city.id
                                    state = new_city.State_Id.id
                                    print(city, state)
                                else:
                                    print('condition is false')
                            characters = string.ascii_letters + string.digits
                            candidate = CandidateMaster(Training_Partner_Id_id=request.session['training_id'],
                                                        Training_Center_Id_id=center_id_get,
                                                        City_Id_id='1', State_Id_id='1', IsDeleted='0', IsActive='0',
                                                        Course_Id_id='1', FirstName=FirstName, LastName=LastName,
                                                        Candidate_password=''.join(random.choice(characters) for i in range(8)),
                                                        Gender=Gender, Candidate_Email=Candidate_Email,
                                                        Phone_no=Phone_no, Address1=Address1, Address2=Address1,
                                                        DOB= now.strftime('%Y-%m-%d'), 
                                                        pincode=pincode,
                                                        adhar_Number=412656565 ,
                                                        willing_to_relocate = willing_to_relocate,
                                                        differently_abled = differently_abled,
                                                        Job_role = job_role,
                                                        Training_Type= training_type,
                                                        Training_Status = training_status,
                                                        Placed_Status = placed_status,
                                                        Qualification=Qualification,
                                                        Training_Scheme_Name = training_scheme_name,
                                                        CreatedBy=candidate_name.Contact_Person_Name,
                                                        CreatedDate=datetime.now(),
                                                        ModifiedBy=candidate_name.Contact_Person_Name,
                                                        ModifiedDate=datetime.now())
                    candidate.save()
            new_length = len(list(filterdata))
            print('new_length', new_length)
            skip_rows = (lines - 1) - new_length
            print('skip_rows', skip_rows)
            if request.method == 'POST':
                new_bulk_upload = bulk_upload(
                    Training_Partner_Id_id = user,
                    Training_Center_Id_id=center_id_get,
                    bulk_upload_file=my_files,
                    TotalRecord=(lines - 1),
                    TotalSkip=skip_rows,
                    TotalSuccess=new_length,
                    UploadedBy=candidate_name.Contact_Person_Name,
                    UploadedDate=datetime.today()
                )
            new_bulk_upload.save()
            return redirect('/Tp/bulkupload/')
 
    return render(request, 'bulkupload.html', {'data': data, 'uid': uid, 'get_center':get_center})
 

def delete_bulk(request, id):
    fetch_id = bulk_upload.objects.get(id=id)
    fetch_id.delete()
    return redirect('/Tp/bulkupload/')
    # messages.error(request, "Training Centerd Deleted Successfully", extra_tags="trainingcenterdelete")
    # return redirect('/Tp/center_list/')

def view_job_post(request):
    # try:
    today = date.today()
    user = request.session['training_id']
    uid = Training_Partner.objects.get(id=user)
    job_post = Job_Posting.objects.filter(IsDeleted=0, Job_Ending_Date__gte =today)
    return render(request, "viewjob.html", {'job_post': job_post, 'uid': uid})
    # except:
    #     messages.error(request,'you have to login first')
    #     return redirect('/Tp/training_login/')

def job_details(request, id):
    # try:
    user = request.session['training_id']
    uid = Training_Partner.objects.get(id=user)
    job_post = Job_Posting.objects.get(id=id)

    return render(request, "job_detail.html", {'job_post': job_post, 'uid': uid})
    # except:
    #     messages.error(request,"you have to login first")
    #     return redirect("/Tp/view_job_post/")
# def apply_job(request,id):
# return render(request,"xyz.html")
def candidate_apply_job(request, id):
    if request.method == "POST":

        job_sts =Job_Posting.objects.get(id=id)
        training_details = request.session['training_id']

        for x in training_details:
            center_details = Training_center.objects.filter(Training_Partner_Id=x.id)

            for y in center_details:
                cn_id = CandidateMaster.objects.filter(id=y.Training_Center_Id)

        print(center_details)

        candid_job_sts = Candidate_job_Status.objects.all()

        for x in candid_job_sts:

            if x.Candidate_Id == cn_id:

                if x.Job_Id == job_sts:

                    messages.error(request, 'Already Applied', extra_tags='already_job_msg')
                    return HttpResponseRedirect('/Tp/job_detail/%d' % job_sts.id)
                else:
                    Candidate_job_Status.objects.create(
                        Candidate_Id=cn_id,
                        Job_Id=job_sts,
                        Job_status='0',
                    )
                messages.error(request, 'Applied Succesfully', extra_tags='job_msg')
                return HttpResponseRedirect('/Tp/job_detail/%d' % job_sts.id)
            else:
                Candidate_job_Status.objects.create(
                    Candidate_Id=cn_id,
                    Job_Id=job_sts,
                    Job_status='0',
                )
                messages.error(request, 'Applied Succesfully', extra_tags='job_msg')
                return HttpResponseRedirect('/Tp/job_detail/%d' % job_sts.id)
        else:
            Candidate_job_Status.objects.create(
                Candidate_Id=cn_id,
                Job_Id=job_sts,
                Job_status='0',
            )
            messages.error(request, 'Applied Succesfully', extra_tags='job_msg')
        return HttpResponseRedirect('/Tp/job_detail/%d' % job_sts.id)

def apply_job(request, id):
    all_job = Job_Posting.objects.get(id=id)
    uid = request.session['training_id']

    all_candidate = CandidateMaster.objects.filter(Training_Partner_Id=uid)
    print("all_candidate : ---------------------",all_candidate)
    not_existed_candid = []
    for x in all_candidate:
        print("x.id : --------------------------",x.id)
        mynew = Candidate_job_Status.objects.filter(Candidate_Id=x.id)
        print('myneew', mynew)
        if Candidate_job_Status.objects.filter(Candidate_Id=x.id).exists():
            pass
    #     else:
    #         not_existed_candid.append(x.id)
    #     print('not_existed_candid :L -------------------',not_existed_candid)
    # for y in not_existed_candid:
    #     print('yyyyyyyyyyyyyy',y)
    #     final_candid = CandidateMaster.objects.filter(id=y)
    #     print('final_candid : -------------------',final_candid)
    #     return render(request,"apply_candidate_list.html",{'final_candid':final_candid})
    return render(request,"apply_candidate_list.html")


def apply_candid_job(request):
    if request.method == 'POST':
        jobb_id = request.POST.get('jobs')
        print("jobb_id: -----------------------",jobb_id)
        candidd_job = request.POST.get('trainingcenter')
        print('candidd_job', candidd_job)
        if candidd_job == None:
            request_job = Job_Posting.objects.get(id=jobb_id)
            messages.error(request, 'Select candiate for applying', extra_tags='appliedcadid')
            return redirect('/Tp/apply_job/%d' % request_job.id)
        else:

            request_candidate = CandidateMaster.objects.get(Candidate_Email=candidd_job)
            print("request_candidate", request_candidate)
            request_job = Job_Posting.objects.get(id=jobb_id)
            print(request_job)  
            Candidate_job_Status.objects.create(
                Candidate_Id=request_candidate,
                Job_Id=request_job,
                Job_status='0')

            return HttpResponseRedirect('/Tp/job_details/%d' % request_job.id)
    else:
        return HttpResponse('You Have to Select A Checkbox')

def view_applied_candidate(request,id):
    user = request.session['training_id']
    uid = Training_Partner.objects.get(id=user)
    print("id :-------------",id)
    request_job = Job_Posting.objects.get(id=id)
    print("request_job : --------------------",request_job)
    all_candid=Candidate_job_Status.objects.filter(Job_Id=request_job).order_by('-id')
    print("all_candid : -----------------------",all_candid)
    return render(request,"applied_candidate.html",{'all_candid':all_candid,'uid':uid})

