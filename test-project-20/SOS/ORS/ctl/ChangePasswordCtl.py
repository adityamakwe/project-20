from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from ..models import User
from ..service.ChangePasswordService import ChangePasswordService
from ..service.EmailService import EmailService
from ..service.EmailMessege import EmailMessege
from ..service.UserService import UserService


class ChangePasswordCtl(BaseCtl):

    def request_to_form(self, requestFrom):
        self.form['id'] = requestFrom['id']
        self.form['oldPassword'] = requestFrom['oldPassword']
        self.form['newPassword'] = requestFrom['newPassword']
        self.form['confirmPassword'] = requestFrom['confirmPassword']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.oldPassword = self.form['oldPassword']
        obj.newPassword = self.form['newPassword']
        obj.confirmPassword = self.form['confirmPassword']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['oldPassword'] = obj.oldPassword
        self.form['newPassword'] = obj.newPassword
        self.form['confirmPassword'] = obj.confirmPassword

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['oldPassword'])):
            inputError['oldPassword'] = "Old Password can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['newPassword'])):
            inputError['newPassword'] = "New Password can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['confirmPassword'])):
            inputError['confirmPassword'] = "Confirm Password can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        user_json = request.session.get('user', None)
        q = User.objects.filter(loginId=user_json.get('loginId'), password=self.form['oldPassword'])
        user = q[0]
        if q.count() > 0:
            if self.form['newPassword'] == self.form['confirmPassword']:
                emailMessege = EmailMessege()
                emailMessege.to = [user.loginId]
                emailMessege.subject = "Change Password"
                mailResponse = EmailService.send(emailMessege, 'changePassword', user)

                # if mailResponse == 1:
                if True:
                    user.password = self.form['newPassword']
                    user.confirmPassword = self.form['confirmPassword']

                    UserService().save(user)

                    self.form['error'] = False
                    self.form['message'] = "your password has been changed successfully, please check your mail..."
                    res = render(request, self.get_template(), {"form": self.form})
                else:
                    self.form['error'] = True
                    self.form['message'] = "Please Check Your Internet Connection"
                    res = render(request, self.get_template(), {"form": self.form})
            else:
                self.form['error'] = True
                self.form['message'] = "Confirm Password are not matched"
                res = render(request, self.get_template(), {"form": self.form})
        else:
            self.form['error'] = True
            self.form['message'] = "Old Password is wrong"
            res = render(request, self.get_template(), {"form": self.form})
        return res

    def get_template(self):
        return "ChangePassword.html"

    def get_service(self):
        return ChangePasswordService()
