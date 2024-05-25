from django.shortcuts import render, redirect
from TrainingPartner.models import *
from django.contrib import messages
import re
from IndustryPartner.models import *
from Candidate_Master.models import *
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from datetime import datetime
import random
from .models import *
from datetime import date

# Create your views here.


def Candid_register(request):
    states = StateMaster.objects.all()
    cource = CourceMaster.objects.all()
    city = CityMaster.objects.all()
    if request.method == "POST":
        City = request.POST.get('DistrictName')
        print("city : -------------",City)
        cityid=CityMaster.objects.get(City_Name = City)
        
        state = request.POST.get('StateName')
        print("state : ---------------",state)
        stateid=StateMaster.objects.get(id=state)
        
        cources = request.POST.get('cource')
        print("cource :--------------------------",cources)
        courceid=CourceMaster.objects.get(id=cources)
        
        firstname = request.POST.get('FirstName')
        lastname = request.POST.get('Lastname')
        email = request.POST.get('Candidate_Email')
        password = request.POST.get('Password')
        phone_number = request.POST.get('Phone_no')
        dob = request.POST.get('DOB')
        address = request.POST.get('Address1')
        address1 = request.POST.get('Address2')
        pincode = request.POST.get('pincode')
        gender = request.POST.get('Gender')
        adhar_number = request.POST.get('Adhar_Number')
        weilling_to_relocate = request.POST.get('willing_to_relocate')
        differently_abled = request.POST.get('differently_abled')
        job_role = request.POST.get('Job_role')
        training_type = request.POST.get('Training_Type')
        training_status = request.POST.get('Training_Status')
        placed_status = request.POST.get('Placed_Status')
        qualification = request.POST.get('Qualification')
        training_scheme_name = request.POST.get('Training_Scheme_Name')
        
        certificate_no = random.randint(100000, 999999)
        otp_genrate = random.randint(100000, 999999)
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            pass   
        else:
            messages.error(request,'Please Enter Valid Email', extra_tags = 'e_msg')
            return render(request,"CM_Register.html",{'city':city,'states':states,'cource': cource,'firstname':firstname,'lastname':lastname,'email':email,'password':password,'phone_number':phone_number,'dob':dob,'address':address,'address1':address1,'pincode':pincode,'gender':gender,'adhar_number':adhar_number,'weilling_to_relocate':weilling_to_relocate,'differently_abled':differently_abled,'job_role':job_role,'training_type':training_type,'training_status':training_status,'placed_status':placed_status,'qualification':qualification,'training_scheme_name':training_scheme_name})
        
        reg = r'\b^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$\b'
        if(re.fullmatch(reg, password)):
            pass
        else:
            messages.error(request,'Your password is weak, Please including Uppercase, Lowercase, Numbers and Special character', extra_tags = 'pwn')
            return render(request,"CM_Register.html",{'city':city,'states':states,'cource': cource,'firstname':firstname,'lastname':lastname,'email':email,'password':password,'phone_number':phone_number,'dob':dob,'address':address,'address1':address1,'pincode':pincode,'gender':gender,'adhar_number':adhar_number,'weilling_to_relocate':weilling_to_relocate,'differently_abled':differently_abled,'job_role':job_role,'training_type':training_type,'training_status':training_status,'placed_status':placed_status,'qualification':qualification,'training_scheme_name':training_scheme_name})
        
        if Candidate_register.objects.filter(Phone_no=phone_number).exists() or Industry_partner.objects.filter(SPOC_Phone=phone_number):
            messages.error(request, "Phone Number is Already Taken, Try With Another Number", extra_tags="phoneverify")
            return render(request,"CM_Register.html",{'city':city,'states':states,'cource': cource,'firstname':firstname,'lastname':lastname,'email':email,'password':password,'phone_number':phone_number,'dob':dob,'address':address,'address1':address1,'pincode':pincode,'gender':gender,'adhar_number':adhar_number,'weilling_to_relocate':weilling_to_relocate,'differently_abled':differently_abled,'job_role':job_role,'training_type':training_type,'training_status':training_status,'placed_status':placed_status,'qualification':qualification,'training_scheme_name':training_scheme_name})
        
        elif Candidate_register.objects.filter(Candidate_Email=email).exists() or Industry_partner.objects.filter(SPOC_Email=email):
            messages.error(request, "Email is Already Taken, Try With Another", extra_tags="emailverify")
            return render(request,"CM_Register.html",{'city':city,'states':states,'cource': cource,'firstname':firstname,'lastname':lastname,'email':email,'password':password,'phone_number':phone_number,'dob':dob,'address':address,'address1':address1,'pincode':pincode,'gender':gender,'adhar_number':adhar_number,'weilling_to_relocate':weilling_to_relocate,'differently_abled':differently_abled,'job_role':job_role,'training_type':training_type,'training_status':training_status,'placed_status':placed_status,'qualification':qualification,'training_scheme_name':training_scheme_name})
        

        createcandidate = Candidate_register(
                                   certificate_number=certificate_no,
                                   City_Id  = cityid,
                                   State_Id=stateid,
                                   Course_Id=courceid,
                                   FirstName=firstname,
                                   LastName=lastname,
                                   Candidate_Email=email,
                                   Candidate_password=password,
                                   Phone_no=phone_number,
                                   DOB=dob,
                                   Address1=address,
                                   Address2=address1,
                                   pincode=pincode,
                                   Gender=gender,
                                   adhar_Number=adhar_number,
                                   willing_to_relocate=weilling_to_relocate,
                                   differently_abled=differently_abled,
                                   Job_Name=job_role,
                                   Training_Type=training_type,
                                   Training_Status=training_status,
                                   Placed_Status=placed_status,
                                   Qualification=qualification,
                                   Training_Scheme_Name=training_scheme_name,
                                   IsDeleted='0',
                                   IsActive='1',
                                   otp=otp_genrate,
                                   otp_is_used='0'
        )
        createcandidate.save()
        return redirect('/cm/')
    else:
        pass
    return render(request,"CM_Register.html",{'states':states, 'cource': cource, 'city': city})


def candidate_login(request):
    
    if request.method == "POST":
        email = request.POST.get('Contact_Person_Email')
        print("Contact_Person_Email : ------------",email)
        passw = request.POST.get('Password')
        print("passw : ------------",passw)

        try:
            tid = Candidate_register.objects.get(Candidate_Email=email)
            print("tid : ------------",tid)

            if email == tid.Candidate_Email:
                if passw == tid.Candidate_password:
                    request.session['candidate_id'] = tid.id
                    request.session['candidate_Email'] = tid.Candidate_Email
                    return redirect('/cm/candidate_dashboard/')
                else:
                    messages.error(request,'invalid cradential', extra_tags = 'log')
                    return render(request,'candidate-login.html')
            else:
                messages.error(request,'invalid cradential', extra_tags = 'log')
                return render(request, 'candidate-login.html')
        except:
            messages.error(request,'invalid cradential', extra_tags = 'log')
            return render(request, 'candidate-login.html')

    else:
        return render(request,"candidate-login.html")
    
    
def candidate_logout(request):
    if 'candidate_id'  in request.session:
        return redirect('/cm/')
    else:
        return render(request, 'candidate-login.html')
    
def candidate_dashboard(request):
    try:
        today = date.today()
        print("today : ----------------",today)
        user = request.session['candidate_id']
        cid = Candidate_register.objects.get(id=user)
        job_post = Job_Posting.objects.filter(IsDeleted = 0, Job_Ending_Date__gte =today )
        

        return render(request,"candidate_dashboard.html",{'cid':cid,'job_post':job_post})
    except:
        messages.error(request,'invalid cradential', extra_tags = 'log')
        return render(request, 'candidate-login.html')

def candidate_profile(request):
    user = request.session['candidate_id']
    cid = Candidate_register.objects.get(id=user)
    CM_View_Profile = Candidate_register.objects.get(id=user)
    return render(request,"CM_profile.html",{'CM_View_Profile':CM_View_Profile,'cid':cid})

def change_password(request):
    return render(request,"CM_change-password.html")

def CM_Update_Profile(request):
    try:
        user = request.session['candidate_id']
        cid = Candidate_register.objects.get(id=user)
        if request.method == "GET":
            CM_Select_Profile = Candidate_register.objects.get(id = request.session['candidate_id'])
            print("CM_Select_Profile :-----------",CM_Select_Profile.id)
            return render(request,"CM_profile_Edit.html",{'CM_Select_Profile':CM_Select_Profile,'cid':cid})
        elif request.method == "POST":
            First_Name = request.POST.get('FirstName')
            Last_name = request.POST.get('LastName')
            gender = request.POST.get('Gender')
            candidate_email = request.POST.get('Candidate_Email')
            phone_no = request.POST.get('Phone_no')
            address1 = request.POST.get('Address1')
            address2 = request.POST.get('Address2')
            pincode = request.POST.get('pincode')
            qualification = request.POST.get('Qualification')
            


            CM_Select_Profile = Candidate_register.objects.get(id = request.session['candidate_id'])
            CM_Select_Profile.FirstName=First_Name
            CM_Select_Profile.LastName=Last_name
            CM_Select_Profile.Gender=gender
            CM_Select_Profile.Candidate_Email=candidate_email 
            CM_Select_Profile.Phone_no=phone_no
            CM_Select_Profile.Address1=address1
            CM_Select_Profile.Address2=address2
            CM_Select_Profile.pincode=pincode
            CM_Select_Profile.Qualification=qualification
            CM_Select_Profile.save()

            return redirect('/cm/candidate_profile')
    except:
        messages.error(request,'You Have To Login First', extra_tags = 'tryexceptlog')
        return redirect("/cm/")


def change_password(request):
    try:
        user = request.session['candidate_id']
        cid = Candidate_register.objects.get(id=user)
        if request.method == "POST":
            old_password=request.POST.get('oldpass')
            print("old :------------",old_password)
            newpassw=request.POST.get('newpassword')
            print("newpassw : -----------",newpassw)
            confirmpassw=request.POST.get('confirmpassword')
            print("confirmpassw : -----------",confirmpassw)
            print("cid.Candidate_password : -----------", cid.Candidate_password)
            if cid.Candidate_password == old_password:
                regex = r'\b^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$\b'
                if(re.fullmatch(regex, newpassw)):
                    pass 
                    if newpassw == confirmpassw:
                        print("(((((((((((((((((((((((((((((((((((((")
                        
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        cid.Candidate_password= newpassw
                        print("cid.Candidate_password = ===========",cid.Candidate_password)
                        cid.save()
                        return redirect('/cm/candidate_profile/')
                
                    else:
                        messages.error(request,'New Password And Confirm Password Does Not Match', extra_tags = 'cmpass')
                        return render(request,"CM_change-password.html",{'cid':cid})
                else:
                    messages.error(request,'Please Enter Strong Password', extra_tags = 'passw')
                    return render(request,"CM_change-password.html",{'cid':cid})
            else:
                messages.error(request,'Please Enter Valid Old Password', extra_tags = 'oldvalidity')
                return render(request,"CM_change-password.html",{'cid':cid})
        else:
            return render(request,"CM_change-password.html",{'cid':cid})
    except:
        messages.error(request,'You Have To Login First', extra_tags = 'tryexceptlog')
        return redirect("/cm/")
        

def all_job_post(request):
    try:
        user = request.session['candidate_id']
        cid = Candidate_register.objects.get(id=user)
        job_post = Job_Posting.objects.filter(IsDeleted = 0)
        return render(request,'view_job.html',{'job_post':job_post,'cid':cid})
    except:
        messages.error(request,'You Have To Login First', extra_tags = 'tryexceptlog')
        return redirect("/cm/")

def job_details(request,id):
    try:
        user = request.session['candidate_id']
        cid = Candidate_register.objects.get(id=user)
        job_post = Job_Posting.objects.get(id=id)
        return render(request,'Job_details.html',{'job_post':job_post,'cid':cid})
    except:
        messages.error(request,'You Have To Login First', extra_tags = 'tryexceptlog')
        return redirect("/cm/")

    
def candidate_apply_job(request,id):
    # try:
        user = request.session['candidate_id']
        cid = Candidate_register.objects.get(id=user)
        print(id)
        job_sts =Job_Posting.objects.get(id=id)
        candidate_details = request.session['candidate_id']
        print(candidate_details)
        cn_id = Candidate_register.objects.get(id=candidate_details)
        print("cn_id : ------------------",cn_id)
        candid_job_sts = Candidate_job_Status.objects.all()
        print("candidate_job_sts : -------------",candid_job_sts)
        for x in candid_job_sts:
            print("x : --------------",x)
            if x.Candidate_Id == cn_id:
                if x.Job_Id == job_sts:             
                    messages.error(request,'Alredy Applied', extra_tags = 'alredy_job_apply_msg')
                    return HttpResponseRedirect('/cm/job_details/%d'%job_sts.id)   
                else:
                    Candidate_job_Status.objects.create(
                    Candidate_Id = cn_id,
                    Job_Id =  job_sts,
                    Job_status = '0',
                )
                messages.error(request,'Applied Succesfully', extra_tags = 'job_msg')
                return HttpResponseRedirect('/cm/job_details/%d'%job_sts.id) 
            else:
                Candidate_job_Status.objects.create(
                    Candidate_Id = cn_id,
                    Job_Id =  job_sts,
                    Job_status = '0',
                )
                messages.error(request,'Applied Succesfully', extra_tags = 'job_msg')
                return HttpResponseRedirect('/cm/job_details/%d'%job_sts.id)
        else:
            Candidate_job_Status.objects.create(
            Candidate_Id = cn_id,
            Job_Id =  job_sts,
            Job_status = '0',
            )
            messages.error(request,'Applied Succesfully', extra_tags = 'job_msg')
        return HttpResponseRedirect('/cm/job_details/%d'%job_sts.id)

    # except:
    #     messages.error(request,'You Have To Login First', extra_tags = 'tryexceptlog')
    #     return redirect("/cm/")


def resume_build(request):
    if request.method == 'GET':

        cid = Candidate_register.objects.get(id=request.session['candidate_id'])
        print("if :-------------------")
        try:
            personalskill = Candidate_personal_detail.objects.get(Candidate_Id=cid.id)
            return render(request, "add-personal.html", {'cid':cid,'personalskill': personalskill})
        except:
            return render(request, "add-personal.html", {'cid': cid, })

    elif request.method == "POST":
        can = Candidate_register.objects.get(id=request.session['candidate_id'])
        print("if :-------------------")
        try:
            personaldetail = Candidate_personal_detail.objects.get(Candidate_Id=can.id)

            Fname = request.POST.get('firstname')
            print(Fname,"First_name:----------------",personaldetail.First_name,"ghdhdgghgggshdghg")
            Lname = request.POST.get('lastname')
            email = request.POST.get('email')
            Phone_number = request.POST.get('Num')
            address = request.POST.get('address')
            current_location = request.POST.get('location')

            personaldetail.First_name = Fname
            personaldetail.Last_name = Lname
            personaldetail.Email = email
            personaldetail.Phone_number =Phone_number
            personaldetail.Address = address
            personaldetail.Current_Location = current_location
            personaldetail.save()
            return redirect('/cm/add_skill/')
        except:
            Fname = request.POST.get('firstname')
            print(Fname, "First_name:----------------")
            Lname = request.POST.get('lastname')
            email = request.POST.get('email')
            Phone_number = request.POST.get('Num')
            address = request.POST.get('address')
            current_location = request.POST.get('location')

            Candidate_personal_detail.objects.create(
                Candidate_Id_id=request.session['candidate_id'],
                First_name=Fname,
                Last_name=Lname,
                Email=email,
                Phone_number=Phone_number,
                Address=address,
                Current_Location=current_location,
            )
            return redirect('/cm/add_skill/')

            
def add_skill(request):
    if request.method == 'GET':

        cid = Candidate_register.objects.get(id=request.session['candidate_id'])
     
        try:
            personalskill = Candidate_skills.objects.get(Candidate_Id=cid.id)
            print('personalskill', personalskill.Skills_Name)
            return render(request, "add-skill.html", {'cid':cid,'personalskill': personalskill})
        except:
            return render(request, "add-skill.html", {'cid': cid})

    elif request.method == "POST":
        can = Candidate_register.objects.get(id=request.session['candidate_id'])
        print("if :-------------------")
        try:
            personaldetail = Candidate_skills.objects.get(Candidate_Id=can.id)

            skillname = request.POST.get('Skills_Name')
       
            

            personaldetail.Skills_Name = skillname
            
            personaldetail.save()
            return redirect('/cm/add_edu/')
        except:
            sname = request.POST.get('Skills_Name')
            
            Candidate_skills.objects.create(
                Candidate_Id_id=request.session['candidate_id'],
                Skills_Name=sname,
                
            )
            return redirect('/cm/add_edu/')


def add_edu(request):
    cid = Candidate_register.objects.get(id=request.session['candidate_id'])
    
    if request.method == "GET":
      
        try:
            education = Candidate_education_detail.objects.get(Candidate_Id=cid)
            
            return render(request, "add-edu.html", {'cid':cid,'education': education})
        except:
            return render(request, "add-edu.html", {'cid': cid})

    elif request.method == "POST":
        cid = Candidate_register.objects.get(id=request.session['candidate_id'])
        print('cid', cid)
        try:
            education = Candidate_education_detail.objects.get(Candidate_Id=cid)
            

            University = request.POST.get('University')
            Passing_year = request.POST.get('Passing_year')
            Persentage = request.POST.get('Persentage')
            Post_graduation = request.POST.get('Post_graduation')

            education.University = University
            education.Passing_year = Passing_year
            education.Persentage = Persentage
            education.Post_graduation = Post_graduation

            education.save()
            return redirect('/cm/add_family/')

        except:
                University = request.POST.get('University')
                Passing_year = request.POST.get('Passing_year')
                Persentage = request.POST.get('Persentage')
                Post_graduation = request.POST.get('Post_graduation')

                Candidate_education_detail.objects.create(
                    Candidate_Id=cid,
                    University=University,
                    Passing_year=Passing_year,
                    Persentage=Persentage,
                    Post_graduation=Post_graduation,
                )
                # educate.save()
                return redirect('/cm/add_family/')


def add_family(request):
    cid = Candidate_register.objects.get(id=request.session['candidate_id'])
    print("cid.id :-------------------------------0", cid.id)

    if request.method == "GET":
        print("if :-------------------")
        try:
            can_family = Candidate_Family_Detail.objects.get(Candidate_Id=cid)
            print("can_family.Sister_Name : ----------", can_family.Sister_Name)
            return render(request, "add-family.html", {'cid': cid, 'can_family': can_family})
        except:
            return render(request, "add-family.html", {'cid': cid})

    elif request.method == "POST":
        Father_Name = request.POST.get('Father_Name')
        Mother_Name = request.POST.get('Mother_Name')
        Brother_Name = request.POST.get('Brother_Name')
        Sister_Name = request.POST.get('Sister_Name')

        cid = Candidate_register.objects.get(id=request.session['candidate_id'])
        print('cid', cid)
        try:
            can_family = Candidate_Family_Detail.objects.get(Candidate_Id=cid)
            print("can_family.University : ----------", can_family.University)


            can_family.Father_Name = Father_Name
            can_family.Mother_Name = Mother_Name
            can_family.Brother_Name = Brother_Name
            can_family.Sister_Name = Sister_Name

            can_family.save()
            return redirect('/cm/add_exp/')

        except:

            add_family = Candidate_Family_Detail(
                Candidate_Id_id = request.session['candidate_id'],
                Father_Name =Father_Name,
                Mother_Name = Mother_Name,
                Brother_Name = Brother_Name,
                Sister_Name = Sister_Name
            )
            add_family.save()
            return redirect('/cm/add_exp/')


def add_exp(request):
    cid = Candidate_register.objects.get(id=request.session['candidate_id'])
    print("cid.id :-------------------------------0", cid.id)

    if request.method == "GET":
        print("if :-------------------")
        try:
            can_experience = Candidate_Experience.objects.get(Candidate_Id=cid)
            print("can_experience.Total_Exp : ----------", can_experience.Total_Exp)
            return render(request, "add-exp.html", {'cid': cid, 'can_experience': can_experience})
        except:
            return render(request, "add-exp.html", {'cid': cid})

    elif request.method == "POST":
        Total_Exp = request.POST.get('Total_Exp')
        Objective = request.POST.get('Objective')
        Profile_Summary = request.POST.get('Profile_Summary')
        Company_Name = request.POST.get('Company_Name')
        Projects = request.POST.get('Projects')

        cid = Candidate_register.objects.get(id=request.session['candidate_id'])
        print('cid', cid)
        try:
            can_experience = Candidate_Experience.objects.get(Candidate_Id=cid)
            print("can_experience.Total_Exp : ----------", can_experience.Total_Exp)

            can_experience.Total_Exp = Total_Exp
            can_experience.Objective = Objective
            can_experience.Profile_Summary = Profile_Summary
            can_experience.Company_Name = Company_Name
            can_experience.Projects = Projects

            can_experience.save()
            return redirect('/cm/download_resume/')

        except:
            add_exp = Candidate_Experience(
                Candidate_Id_id = request.session['candidate_id'],
                Total_Exp = Total_Exp,
                Objective = Objective,
                Profile_Summary = Profile_Summary,
                Company_Name = Company_Name,
                Projects = Projects
             )
            add_exp.save()



            return redirect('/cm/download_resume/')


def download_resume(request):
    user = request.session['candidate_Email']
    cid = Candidate_register.objects.get(Candidate_Email=user)
    personaldetail = Candidate_personal_detail.objects.get(Candidate_Id=cid)
    print('personaldetail: ---------------',personaldetail)
    skilldetail = Candidate_skills.objects.get(Candidate_Id=cid)
    educationdetail = Candidate_education_detail.objects.get(Candidate_Id=cid)
    familydetail = Candidate_Family_Detail.objects.get(Candidate_Id=cid)
    experiencedetail = Candidate_Experience.objects.get(Candidate_Id=cid)
    return render(request,'download_resume.html',{'cid':cid,'personaldetail':personaldetail,'skilldetail':skilldetail,'educationdetail':educationdetail,'familydetail':familydetail,'experiencedetail':experiencedetail})



def filter_job(request):
    
    all_job = Job_Posting.objects.all()
    user = request.session['candidate_Email']
    cid = Candidate_register.objects.get(Candidate_Email=user)
    states = StateMaster.objects.all()
    Cource = CourceMaster.objects.all()
    city = CityMaster.objects.all()
    if ('q' in request.GET) or ('findstate' in request.GET) or ('findcity' in request.GET):
        value = request.GET.get('q', '').split(" ")
        fin = Job_Posting.objects.filter(Job_Name__icontains=value[0])
        my_value = []
        for val in fin:
            value = request.GET.get('findstate')
            find_city = request.GET.get('findcity')
            
            if value == '' : 
                my_value.append(val)
            elif int(value) == val.State_id_id:
                my_value.append(val)
            elif int(find_city) == val.City_id_id:
                my_value.append(val)
            else:
                pass
        
        return render(request,"filter_job.html",{'states':states, 'my_value': my_value, 'cid': cid, 'all_job': all_job, 'city': city})
    return render(request,"filter_job.html",{'states':states, 'cid': cid, 'all_job': all_job, 'city': city})
