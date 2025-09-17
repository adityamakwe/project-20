from django.shortcuts import render
from .BaseCtl import BaseCtl
from ..service.EmailMessege import EmailMessege
from ..service.EmailService import EmailService
from ..utility.DataValidator import DataValidator
from ..models import User
from ..service.UserService import UserService


class RegistrationCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['firstName'] = requestForm['firstName']
        self.form['lastName'] = requestForm['lastName']
        self.form['loginId'] = requestForm['loginId']
        self.form['password'] = requestForm['password']
        self.form['confirmPassword'] = requestForm['confirmPassword']
        self.form['dob'] = requestForm['dob']
        self.form['address'] = requestForm['address']
        self.form['gender'] = requestForm['gender']
        self.form['mobileNumber'] = requestForm['mobileNumber']
        self.form['roleId'] = 2
        self.form['roleName'] = 'Student'

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.firstName = self.form['firstName']
        obj.lastName = self.form['lastName']
        obj.loginId = self.form['loginId']
        obj.password = self.form['password']
        obj.confirmPassword = self.form['confirmPassword']
        obj.dob = self.form['dob']
        obj.address = self.form['address']
        obj.gender = self.form['gender']
        obj.mobileNumber = self.form['mobileNumber']
        obj.roleId = self.form['roleId']
        obj.roleName = self.form['roleName']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['firstName'])):
            inputError['firstName'] = "First Name is required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['firstName'])):
                inputError['firstName'] = "First Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['lastName'])):
            inputError['lastName'] = "Last Name is required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['lastName'])):
                inputError['lastName'] = "Last Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["loginId"])):
            inputError["loginId"] = "Login ID is required"
            self.form["error"] = True
        else:
            if (DataValidator.isemail(self.form['loginId'])):
                inputError['loginId'] = "login ID must be like student@gmail.com"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['password'])):
            inputError['password'] = "Password is required"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['confirmPassword'])):
            inputError['confirmPassword'] = "Confirm Passsword is required"
            self.form['error'] = True

        if (DataValidator.isNotNull(self.form['confirmPassword'])):
            if self.form['password'] != self.form['confirmPassword']:
                inputError['confirmPassword'] = "Password and Confirmpassword are not same"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "DOB is required"
            self.form["error"] = True
        else:
            if (DataValidator.isDate(self.form['dob'])):
                inputError['dob'] = "Incorrect Date"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['address'])):
            inputError['address'] = "Address is required"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['gender'])):
            inputError['gender'] = "Gender is required"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['mobileNumber'])):
            inputError['mobileNumber'] = "Mobile Number is required"
            self.form['error'] = True
        else:
            if (DataValidator.ismobilecheck(self.form['mobileNumber'])):
                inputError['mobileNumber'] = "Enter Correct Mobile No."
                self.form['error'] = True
        return self.form['error']

    def display(self, request, params={}):
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        duplicate = self.get_service().get_model().objects.filter(loginId=self.form['loginId'])
        if duplicate.count() > 0:
            self.form['error'] = True
            self.form['message'] = "Login Id already exist"
            res = render(request, self.get_template(), {'form': self.form})
        else:
            emailMessege = EmailMessege()
            emailMessege.to = [self.form['loginId']]
            emailMessege.subject = "ORS Registration Successful"

            e = {}
            e['loginId'] = self.form['loginId']
            e['password'] = self.form['password']

            mailResponse = EmailService.send(emailMessege, 'signUp', e)

            if mailResponse:
                r = self.form_to_model(User())
                self.get_service().save(r)
                self.form['error'] = False
                self.form['message'] = "User Registration successfully..!!"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                self.form['error'] = True
                self.form['message'] = "Please Check Your Internet Connection"
                res = render(request, self.get_template(), {'form': self.form})
            return res

    def get_template(self):
        return "Registration.html"

    def get_service(self):
        return UserService()
