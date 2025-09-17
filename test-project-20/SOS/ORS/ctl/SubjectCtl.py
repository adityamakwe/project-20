from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from ..models import Subject
from ..service.SubjectService import SubjectService
from ..service.CourseService import CourseService


class SubjectCtl(BaseCtl):

    def preload(self, request, params={}):
        self.dynamic_preload = CourseService().preload()

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['description'] = requestForm['description']
        self.form['courseId'] = requestForm['courseId']
        if self.form['courseId'] != '':
            course = CourseService().get(self.form['courseId'])
            self.form["courseName"] = course.name

    def form_to_model(self, obj):
        course = CourseService().get(self.form['courseId'])
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.name = self.form['name']
        obj.description = self.form['description']
        obj.courseId = self.form['courseId']
        obj.courseName = course.name
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['description'] = obj.description
        self.form['courseId'] = obj.courseId
        self.form['courseName'] = obj.courseName

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Subject Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "Subject Description can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['courseId'])):
            inputError['courseId'] = "Course can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            id = params['id']
            subject = self.get_service().get(id)
            self.model_to_form(subject)
        res = render(request, self.get_template(), {'form': self.form, 'courseList': self.dynamic_preload})
        return res

    def submit(self, request, params={}):
        if (params['id'] > 0):
            pk = params['id']
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(name=self.form['name'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Subject Name already exists"
                res = render(request, self.get_template(), {'form': self.form, 'courseList': self.dynamic_preload})
            else:
                subject = self.form_to_model(Subject())
                self.get_service().save(subject)
                self.form['id'] = subject.id
                self.form['error'] = False
                self.form['message'] = "Subject updated successfully"
                res = render(request, self.get_template(), {'form': self.form, 'courseList': self.dynamic_preload})
        else:
            duplicate = self.get_service().get_model().objects.filter(name=self.form['name'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Subject Name already exists"
                res = render(request, self.get_template(), {'form': self.form, 'courseList': self.dynamic_preload})
            else:
                subject = self.form_to_model(Subject())
                self.get_service().save(subject)
                self.form['error'] = False
                self.form['message'] = "Subject added successfully"
                res = render(request, self.get_template(), {'form': self.form, 'courseList': self.dynamic_preload})
        return res

    def get_template(self):
        return "Subject.html"

    def get_service(self):
        return SubjectService()
