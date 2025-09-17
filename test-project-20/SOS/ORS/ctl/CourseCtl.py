from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from ..models import Course
from ..service.CourseService import CourseService


class CourseCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['description'] = requestForm['description']
        self.form['duration'] = requestForm['duration']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.description = self.form['description']
        obj.duration = self.form['duration']
        return obj

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['description'] = obj.description
        self.form['duration'] = obj.duration

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Course Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Course Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "Course Description can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['duration'])):
            inputError['duration'] = "Course Duration can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            course = self.get_service().get(params['id'])
            self.model_to_form(course)
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        if params['id'] > 0:
            pk = params['id']
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(name=self.form['name'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Course Name already exists"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                r = self.form_to_model(Course())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] = "Course updated successfully"
                res = render(request, self.get_template(), {'form': self.form})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(name=self.form['name'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Course Name already exists"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                course = self.form_to_model(Course())
                self.get_service().save(course)
                self.form['error'] = False
                self.form['message'] = "Course added successfully"
                res = render(request, self.get_template(), {'form': self.form})
            return res

    def get_template(self):
        return "Course.html"

    def get_service(self):
        return CourseService()
