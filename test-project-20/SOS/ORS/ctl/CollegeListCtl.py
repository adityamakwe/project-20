from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ..utility.DataValidator import DataValidator
from ..models import College
from ..service.CollegeService import CollegeService


class CollegeListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['name'] = requestForm.get("name", None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        CollegeListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = College.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        CollegeListCtl.count += 1
        self.form['pageNo'] = CollegeListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = College.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        CollegeListCtl.count -= 1
        self.form['pageNo'] = CollegeListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def new(self, request, params={}):
        res = redirect("/ORS/College/")
        return res

    def submit(self, request, params={}):
        CollegeListCtl.count = 1
        self.form['pageNo'] = CollegeListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['error'] = True
            self.form['message'] = "No record found"
        ress = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return ress

    def deleteRecord(self, request, params={}):
        if not self.form['ids']:
            self.form['error'] = True
            self.form['message'] = "Please select at least one checkbox"
        else:
            for id in self.form['ids']:
                id = int(id)
                college = self.get_service().get(id)
                if college:
                    self.get_service().delete(id)
                    self.form['error'] = False
                    self.form['message'] = "Data has been deleted successfully"
                else:
                    self.form['error'] = True
                    self.form['message'] = "Data was not deleted"

        self.form['pageNo'] = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = College.objects.last().id
        return render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})

    def get_template(self):
        return "CollegeList.html"

    def get_service(self):
        return CollegeService()
