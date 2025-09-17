from django.shortcuts import render, redirect
from .BaseCtl import BaseCtl
from ..models import User
from ..service.RoleService import RoleService
from ..service.UserService import UserService


class UserListCtl(BaseCtl):
    count = 1

    def preload(self, request, params={}):
        self.dynamic_preload = RoleService().preload()

    def request_to_form(self, requestForm):
        self.form['firstName'] = requestForm.get("firstName", None)
        self.form['ids'] = requestForm.getlist('ids', None)
        self.form['dob'] = requestForm.get('dob', None)
        self.form['roleId'] = requestForm.get('roleId', None)
        if self.form['roleId'] != '':
            role = RoleService().get(self.form['roleId'])
            self.form["roleName"] = role.name

    def display(self, request, params={}):
        UserListCtl.count = self.form['pageNo']
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = User.objects.last().id
        res = render(request, self.get_template(),
                     {'pageList': self.page_list, 'form': self.form, 'roleList': self.dynamic_preload})
        return res

    def next(self, request, params={}):
        UserListCtl.count += 1
        self.form['pageNo'] = UserListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = User.objects.last().id
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def previous(self, request, params={}):
        UserListCtl.count -= 1
        self.form['pageNo'] = UserListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def new(self, request, params={}):
        res = redirect("/ORS/User/")
        return res

    def deleteRecord(self, request, params={}):
        if not self.form['ids']:
            self.form['error'] = True
            self.form['message'] = "Please select at least one checkbox"
        else:
            for id in self.form['ids']:
                id = int(id)
                user = self.get_service().get(id)
                if user:
                    self.get_service().delete(id)
                    self.form['error'] = False
                    self.form['message'] = "Data has been deleted successfully"
                else:
                    self.form['error'] = True
                    self.form['message'] = "Data was not deleted"

        self.form['pageNo'] = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = User.objects.last().id
        return render(request, self.get_template(),
                      {'pageList': self.page_list, 'form': self.form, 'roleList': self.dynamic_preload})

    def submit(self, request, params={}):
        UserListCtl.count = 1
        self.form['pageNo'] = UserListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        if self.page_list == []:
            self.form['error'] = True
            self.form['message'] = "No record found"
        res = render(request, self.get_template(),
                     {'pageList': self.page_list, 'form': self.form, 'roleList': self.dynamic_preload})
        return res

    def get_template(self):
        return "UserList.html"

    def get_service(self):
        return UserService()
