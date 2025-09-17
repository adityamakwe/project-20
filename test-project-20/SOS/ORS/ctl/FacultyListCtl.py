from django.shortcuts import render, redirect
from .BaseCtl import BaseCtl
from ..models import Faculty
from ..service.FacultyService import FacultyService


class FacultyListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['firstName'] = requestForm.get('firstName', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        FacultyListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Faculty.objects.last().id
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def next(self, request, params={}):
        FacultyListCtl.count += 1
        self.form['pageNo'] = FacultyListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Faculty.objects.last().id
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def previous(self, request, params={}):
        FacultyListCtl.count -= 1
        self.form['pageNo'] = FacultyListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def submit(self, request, params={}):
        FacultyListCtl.count = 1
        self.form['pageNo'] = FacultyListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['error'] = True
            self.form['message'] = "No record found"
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def new(self, request, params={}):
        res = redirect("/ORS/Faculty/")
        return res

    def deleteRecord(self, request, params={}):
        if not self.form['ids']:
            self.form['error'] = True
            self.form['message'] = "Please select at least one checkbox"
        else:
            for id in self.form['ids']:
                id = int(id)
                faculty = self.get_service().get(id)
                if faculty:
                    self.get_service().delete(id)
                    self.form['error'] = False
                    self.form['message'] = "Data has been deleted successfully"
                else:
                    self.form['error'] = True
                    self.form['message'] = "Data was not deleted"

        self.form['pageNo'] = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Faculty.objects.last().id
        return render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})

    def get_template(self):
        return "FacultyList.html"

    def get_service(self):
        return FacultyService()
