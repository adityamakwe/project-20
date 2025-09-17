from django.shortcuts import render
from .BaseCtl import BaseCtl
from ..service.FacultyService import FacultyService
from ..utility.DataValidator import DataValidator
from ..models import Faculty
from ..service.CollegeService import CollegeService
from ..service.CourseService import CourseService
from ..service.SubjectService import SubjectService


class FacultyCtl(BaseCtl):

    def preload(self, request, params={}):
        self.college_List = CollegeService().preload()
        self.course_List = CourseService().preload()
        self.subject_List = SubjectService().preload()

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['firstName'] = requestForm['firstName']
        self.form['lastName'] = requestForm['lastName']
        self.form['email'] = requestForm['email']
        self.form['password'] = requestForm['password']
        self.form['address'] = requestForm['address']
        self.form['gender'] = requestForm['gender']
        self.form['dob'] = requestForm['dob']
        self.form['collegeId'] = requestForm['collegeId']
        self.form['courseId'] = requestForm['courseId']
        self.form['subjectId'] = requestForm['subjectId']

        if self.form['collegeId'] != '':
            college = CollegeService().get(self.form['collegeId'])
            self.form["collegeName"] = college.name

        if self.form['courseId'] != '':
            course = CourseService().get(self.form['courseId'])
            self.form["courseName"] = course.name

        if self.form['subjectId'] != '':
            subject = SubjectService().get(self.form['subjectId'])
            self.form["subjectName"] = subject.name

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['firstName'] = obj.firstName
        self.form['lastName'] = obj.lastName
        self.form['email'] = obj.email
        self.form['password'] = obj.password
        self.form['address'] = obj.password
        self.form['gender'] = obj.gender
        self.form['dob'] = obj.dob.strftime("%Y-%m-%d")
        self.form['collegeId'] = obj.collegeId
        self.form['courseId'] = obj.courseId
        self.form['subjectId'] = obj.subjectId
        self.form['collegeName'] = obj.collegeName
        self.form['courseName'] = obj.courseName
        self.form['subjectName'] = obj.subjectName

    def form_to_model(self, obj):
        college = CollegeService().get(self.form['collegeId'])
        course = CourseService().get(self.form['courseId'])
        subject = SubjectService().get(self.form['subjectId'])
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.firstName = self.form['firstName']
        obj.lastName = self.form['lastName']
        obj.email = self.form['email']
        obj.password = self.form['password']
        obj.address = self.form['address']
        obj.dob = self.form['dob']
        obj.gender = self.form['gender']
        obj.collegeId = self.form['collegeId']
        obj.courseId = self.form['courseId']
        obj.subjectId = self.form['subjectId']
        obj.collegeName = college.name
        obj.courseName = course.name
        obj.subjectName = subject.name
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['firstName'])):
            inputError['firstName'] = "First Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['firstName'])):
                inputError['firstName'] = "First Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['lastName'])):
            inputError['lastName'] = "Last Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['lastName'])):
                inputError['lastName'] = "Last Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['email'])):
            inputError['email'] = "Email can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isemail(self.form['email'])):
                inputError['email'] = "Email must be like student@gmail.com"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['password'])):
            inputError['password'] = "password can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['address'])):
            inputError['address'] = "Address can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['gender'])):
            inputError['gender'] = "Gender can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['dob'])):
            inputError['dob'] = "DOB can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['dob'])):
                inputError['dob'] = "Incorrect date format, should be YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['courseId'])):
            inputError['courseId'] = "Course can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['collegeId'])):
            inputError['collegeId'] = "College can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['subjectId'])):
            inputError['subjectId'] = "Subject can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            id = params['id']
            faculty = self.get_service().get(id)
            self.model_to_form(faculty)
        res = render(request, self.get_template(), {
            'form': self.form,
            'collegeList': self.college_List,
            'courseList': self.course_List,
            'subjectList': self.subject_List
        })
        return res

    def submit(self, request, params={}):
        if (params['id'] > 0):
            pk = params['id']
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(email=self.form['email'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Email already exists"
                res = render(request, self.get_template(), {
                    'form': self.form,
                    'collegeList': self.college_List,
                    'courseList': self.course_List,
                    'subjectList': self.subject_List
                })
            else:
                faculty = self.form_to_model(Faculty())
                self.get_service().save(faculty)
                self.form['id'] = faculty.id
                self.form['error'] = False
                self.form['message'] = "Faculty updated successfully"
                res = render(request, self.get_template(), {
                    'form': self.form,
                    'collegeList': self.college_List,
                    'courseList': self.course_List,
                    'subjectList': self.subject_List
                })
        else:
            duplicate = self.get_service().get_model().objects.filter(email=self.form['email'])
            if (duplicate.count() > 0):
                self.form['error'] = True
                self.form['message'] = "Email already exists"
                res = render(request, self.get_template(), {
                    'form': self.form,
                    'collegeList': self.college_List,
                    'courseList': self.course_List,
                    'subjectList': self.subject_List
                })
            else:
                faculty = self.form_to_model(Faculty())
                self.get_service().save(faculty)
                self.form['error'] = False
                self.form['message'] = "Faculty added successfully"
                res = render(request, self.get_template(), {
                    'form': self.form,
                    'collegeList': self.college_List,
                    'courseList': self.course_List,
                    'subjectList': self.subject_List
                })
        return res

    def get_template(self):
        return "Faculty.html"

    def get_service(self):
        return FacultyService()
