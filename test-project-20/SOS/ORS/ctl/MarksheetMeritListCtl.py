from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..service.MarksheetMeritListService import MarksheetMeritListService


class MarksheetMeritListCtl(BaseCtl):
    count = 1

    def display(self, request, params={}):
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def submit(self, request, params={}):
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def get_template(self):
        return "MarksheetMeritList.html"

    def get_service(self):
        return MarksheetMeritListService()
