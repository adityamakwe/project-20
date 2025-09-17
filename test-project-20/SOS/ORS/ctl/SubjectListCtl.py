from django.shortcuts import render, redirect
from ..models import Subject
from .BaseCtl import BaseCtl
from ..service.SubjectService import SubjectService


class SubjectListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['name'] = requestForm.get('name', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        SubjectListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Subject.objects.last().id
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def next(self, request, params={}):
        SubjectListCtl.count += 1
        self.form['pageNo'] = SubjectListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Subject.objects.last().id
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def previous(self, request, params={}):
        SubjectListCtl.count -= 1
        self.form['pageNo'] = SubjectListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def submit(self, request, params={}):
        SubjectListCtl.count = 1
        self.form['pageNo'] = SubjectListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['error'] = True
            self.form['message'] = "No record found"
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def deleteRecord(self, request, params={}):
        if not self.form['ids']:
            self.form['error'] = True
            self.form['message'] = "Please select at least one checkbox"
        else:
            for id in self.form['ids']:
                id = int(id)
                subject = self.get_service().get(id)
                if subject:
                    self.get_service().delete(id)
                    self.form['error'] = False
                    self.form['message'] = "Data has been deleted successfully"
                else:
                    self.form['error'] = True
                    self.form['message'] = "Data was not deleted"

        self.form['pageNo'] = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Subject.objects.last().id
        return render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})

    def new(self, request, params={}):
        res = redirect("/ORS/Subject/")
        return res

    def get_template(self):
        return "SubjectList.html"

    def get_service(self):
        return SubjectService()
