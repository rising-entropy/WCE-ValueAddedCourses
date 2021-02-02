import os
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views import generic
from django.views.generic.base import View
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.base import View
from student.models import student as Student
from student.models import enrolledStudent
from django.contrib.auth.hashers import check_password
#from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
import mimetypes

class landingPage(View):
    
    def get(self, request, template_name='landingPage.html'):
        try:
            stud = Student.objects.filter(user = request.user)
            stud = stud[0]
            message={'message':'message'}
            if (stud.PaidAttendenceCertificateDL or stud.PaidAttendenceDL)  and  (stud.PaidAttendencePython   or stud.PaidAttendenceCertificatePython):
                    message['message']= 'PyandDL'
            elif (stud.PaidAttendenceCertificateDL or stud.PaidAttendenceDL) :
                    message['message']= 'DL'
            elif (stud.PaidAttendencePython   or stud.PaidAttendenceCertificatePython):
                    message['message']= 'python'
            else :
                message['message']= 'nothing'
        except:
            message={'message':'message'}
            message['message']= 'nothing'
        return render(request, template_name, message)

class register(View):

    def get(self, request, template_name='register.html'):
        return render(request, template_name)

    def post(self, request, template_name='register.html'):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        designation = request.POST.get('designation')
        organisation = request.POST.get('organisation')
        address = request.POST.get('address')
        phoneNumber = request.POST.get('phoneNumber')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confPassword = request.POST.get('conf_password')
        profilePicture = request.POST.get('profilePicture')
        if password != confPassword:
            err = {'error_message': "Password don't match. Please Try Again."}
            return render(request, 'register.html', err)

        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            user.save()
        except:
            err = {}
            err['error_message'] = "Account with this Username or Email already exists."
            return render(request, template_name, err)

        try:
            studentData = Student(user=user, designation=designation, organisation=organisation, address=address, phoneNumber=phoneNumber, profilePicture=profilePicture)
            studentData.save()
        except:
            err = {}
            err['error_message'] = "Account with this Username already exists."
            return render(request, template_name, err)

        my_group = Group.objects.get(name='student_group')
        my_group.user_set.add(user)

        err = {}
        err['error_message'] = "Registration Successful. Please Login."
        return render(request, template_name,err)

class Login(View):

    def get(self, request, template_name='login.html'):
        return render(request, template_name)

    def post(self, request, template_name='login.html'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        group = None
        if user is not None:
            login(request, user)
            userr = Group.objects.filter(user=user)
            group = user.groups.all()[0].name
            if group == 'student_group':
                return redirect('landingPage')
            elif group == 'faculty_group':
                return redirect('facultyLandingPage')
            else:
                return render(request, 'landingPage.html', {})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('landingPage')

class profile(View):

    def get(self, request, template_name='profile.html'):
        stud = Student.objects.filter(user = request.user)
        stud = stud[0]
        print(stud.profilePicture)
        err = {}
        err["student"] = stud
        return render(request, template_name, err)

    def post(self, request, template_name='profile.html'):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        designation = request.POST.get('designation')
        organisation = request.POST.get('organisation')
        address = request.POST.get('address')
        phoneNumber = request.POST.get('phoneNumber')
        email = request.POST.get('email')
        profilePicture = request.POST.get('profilePicture')

        studentData = Student.objects.filter(user=request.user)
        studentData = studentData[0]
        organisation = organisation.rstrip()
        organisation = organisation.lstrip()
        address = address.rstrip()
        address = address.lstrip()
        phoneNumber = phoneNumber.rstrip()
        phoneNumber = phoneNumber.lstrip()

        if organisation == "":
            organisation = studentData.organisation
        if address == "":
            address = studentData.address
        if phoneNumber == "":
            phoneNumber = studentData.phoneNumber

        # Update the Fields
        try:
            Student.objects.filter(user=request.user).update(organisation=organisation, address=address, phoneNumber=phoneNumber, profilePicture=profilePicture)
        except:
            err = {}
            err["error_message"] = "Some Error Occurred. Please Try Again."
            return render(request, template_name, err)
        
        stud = Student.objects.filter(user = request.user)
        stud = stud[0]
        err = {}
        err["student"] = stud
        err["error_message"] = "Changes Saved Successfully."
        return render(request, template_name, err)

class changePassword(View):

    def get(self, request, template_name = "changepassword.html"):
        return render(request, template_name)

    def post(self, request, template_name = "changepassword.html"):
        currPassword = request.POST.get('currentPassword')
        newPassword = request.POST.get('newPassword')
        confPassword = request.POST.get('reNewPassword')

        try:
            matchcheck= check_password(currPassword, request.user.password)
            if matchcheck is False:
                err = {}
                err["error_message"]= "Entered Current Password is Incorrect. Please Retry."
                return render(request, template_name, err)
            if newPassword != confPassword:
                err = {}
                err["error_message"]= "Entered New Passwords don't Match. Please Retry."
                return render(request, template_name, err)
        except:
            err = {}
            err["error_message"]= "Refresh the Page to change the Password Again."
            return render(request, template_name, err)

        U=User.objects.get(username=request.user.username)
        U.set_password(newPassword)
        U.save()
        update_session_auth_hash(request,U)
        stud = Student.objects.filter(user = request.user)
        stud = stud[0]
        err = {}
        err["student"] = stud
        err["error_message"] = "Password changed successfully."
        return render(request, 'profile.html', err)
        

class pythonForEverybody(View):

    def get(self, request, template_name = 'pythonForEverybody.html'):
        message={'message':'message'}
        try:
            stud = Student.objects.filter(user = request.user)
            stud =stud[0]
            if stud.PaidAttendencePython is True:
                message['message']='Enrolled without certification'
            elif stud.PaidAttendenceCertificatePython is True:
                message['message']='Enrolled for certification'
            else:
                message['message']='Enroll'
        except:
            message['message']='Login to Enroll'
        return render(request, template_name,message)



class about(View):
    def get(self, request, template_name = 'about.html'):
        return render(request, template_name)

class deepLearning(View):
    def get(self, request, template_name = 'deepLearning.html'):    
        message={'message':'message'}
        try:
            stud = Student.objects.filter(user = request.user)
            stud =stud[0]
            if stud.PaidAttendenceDL is True:
                message['message']='Enrolled without certification'
            elif stud.PaidAttendenceCertificateDL is True:
                message['message']='Enrolled for certification'
            else:
                message['message']='Enroll'
        except:
            message['message']='Login to Enroll'
        return render(request, template_name, message)

class enrollPython(View):

    def get(self,request,template_name='summaryPython.html'):
        try:
            stud = Student.objects.filter(user = request.user)
            stud =stud[0]
            err = {}
            err["student"] = stud
            return render(request,template_name, err)
        except:
            return render(request,'login.html')
    
    def post(self,request,template_name='summaryPython.html'):
        paymentType = request.POST.get('paymentType')
        paymentID = request.POST.get('paymentID')
        screenShot = request.POST.get('screenShot')
        
        enrolled_stud = request.user
        enrollType=request.POST.get('enrollType')
        err={}
        stud = Student.objects.filter(user=request.user)
        stud = stud[0]
        err['student']= stud
        if enrollType == '1' and stud.PaidAttendencePython == True:
            #already enrolled
            err["error_message"] = "You Have Already Enrolled For The Course without Certificate."
            return render(request,template_name, err)
        elif enrollType == '2' and stud.PaidAttendenceCertificatePython == True:
            #already enrolled
            err["error_message"] = "You Have Already Enrolled For The Course with Certificate."
            return render(request,template_name, err)
        elif enrollType == '1':
            amount = 1500
            err["amount"]=1500
            Student.objects.filter(user=request.user).update(PaidAttendencePython=True)
            err["enrollType"]="Python for Everybody: Attendance"
        elif enrollType == '2':
            amount = 2000
            err["amount"]=2000
            Student.objects.filter(user=request.user).update(PaidAttendenceCertificatePython=True)
            err["enrollType"]="Python for Everybody: Attendance + Certificate"
        try:
            enrolledStudentData = enrolledStudent(amount=amount, paymentID=paymentID, paymentType=paymentType,screenShot=screenShot,enrolled_stud=stud)
            enrolledStudentData.save()
            err['error_message']="Enrolled successfully for the course."
        except:
            err['error_message']="Problem with Adding the Transaction Details."
            return render(request, 'enrollPython.html', err)
        return render(request, 'successPython.html', err)

class enrollDL(View):

    def get(self,request,template_name='summaryDL.html'):
        stud = Student.objects.filter(user = request.user)
        stud =stud[0]
        err = {}
        err["student"] = stud
        return render(request,template_name, err)
    
    def post(self,request,template_name='summaryDL.html'):
        paymentID = request.POST.get('paymentID')
        paymentType = request.POST.get('paymentType')
        enrolled_stud = request.user
        screenShot = request.POST.get('screenShot')
        enrollType = request.POST.get('enrollType')
        if enrollType == '1':
            amount = 2500
        elif enrollType == '2':
            amount = 3000
        err = {}
        stud = Student.objects.filter(user = request.user)
        stud =stud[0]
        enrolled_stud = stud
        if enrollType == '1' and stud.PaidAttendenceDL == True:
            #already enrolled
            stud = Student.objects.filter(user = request.user)
            stud =stud[0]
            err["student"] = stud
            err["error_message"] = "You Have Already Enrolled For The Course without Certificate."
            return render(request,template_name, err)
        elif enrollType == '2' and stud.PaidAttendenceCertificateDL == True:
            #already enrolled
            stud = Student.objects.filter(user = request.user)
            stud =stud[0]
            err["student"] = stud
            err["error_message"] = "You Have Already Enrolled For The Course with Certificate."
            return render(request,template_name, err)
        elif enrollType == '1':
            Student.objects.filter(user = request.user).update(PaidAttendenceDL = True)
        elif enrollType == '2':
            Student.objects.filter(user = request.user).update(PaidAttendenceCertificateDL = True)
        
        try:
            enrolledstudentData = enrolledStudent(paymentID=paymentID, screenShot=screenShot, paymentType=paymentType, enrolled_stud=enrolled_stud, amount=amount)
            enrolledstudentData.save()
        except:
            stud = Student.objects.filter(user = request.user)
            stud =stud[0]
            err["student"] = stud
            err["error_message"] = "Problem with Adding the Transaction Details."
            return render(request,template_name, err)
        
        err["error_message"] = "Enrolled Successfully for the Course."

        return render(request, 'successDL.html', err)

        
def isFaculty(group_name):
    if group_name == 'faculty_group':
        return 1
    else:
        return 0

class facultyLandingPage(View):
    def get(self, request, template_name="facultyLandingPage.html"):
        try:
            group = request.user.groups.all()[0].name
            if isFaculty(group) == 0:
                return render(request, 'login.html')
            return render(request, template_name)
        except:
            return render(request, 'login.html')

class enrollListPython(View):
    def get(self, request, template_name="enrollListPython.html"):
        
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            enrollList ={}
            enrollList['attend']= Student.objects.filter(PaidAttendencePython=True)
            enrollList['certificate'] = Student.objects.filter(PaidAttendenceCertificatePython=True)
        return render(request, template_name,enrollList)
        

class enrollListDL(View):
    def get(self, request, template_name="enrollListDL.html"):
        try:
            group = request.user.groups.all()[0].name
            if isFaculty(group) == 0:
                return render(request, 'login.html')
            else:
                enrollList ={}
                enrollList['attend']= Student.objects.filter(PaidAttendenceDL=True)
                enrollList['certificate'] = Student.objects.filter(PaidAttendenceCertificateDL=True)
            return render(request, template_name,enrollList)
        except:
            return render(request, 'login.html')

class paymentDetailsPy(View):
    def get(self,request,stud,template_name="paymentDetailsPy.html"):
        thatStud = User.objects.filter(email = stud)
        thatStud = thatStud[0]
        thatStud = Student.objects.filter(user=thatStud)
        thatStud = thatStud[0]
        enrolled_stud = enrolledStudent.objects.filter(enrolled_stud=thatStud)
        for i in enrolled_stud:
            if i.amount=="1500" or i.amount=="2000":
                student=i
        enroll_details={}
        enroll_details['student']=student
        return render(request,template_name, enroll_details)

class paymentDetailsDL(View):
    def get(self,request,stud,template_name="paymentDetailsDL.html"):
        thatStud = User.objects.filter(email = stud)
        thatStud = thatStud[0]
        thatStud = Student.objects.filter(user=thatStud)
        thatStud = thatStud[0]
        enrolled_stud = enrolledStudent.objects.filter(enrolled_stud=thatStud)
        for i in enrolled_stud:
            if i.amount=="2500" or i.amount=="3000":
                student=i
        enroll_details={}
        enroll_details['student']=student
        return render(request,template_name, enroll_details)

