from django.db import models


class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    loginId = models.EmailField()
    password = models.CharField(max_length=20)
    confirmPassword = models.CharField(max_length=20, default='')
    dob = models.DateField(max_length=20)
    address = models.CharField(max_length=50, default='')
    gender = models.CharField(max_length=50, default='')
    mobileNumber = models.CharField(max_length=50, default='')
    roleId = models.IntegerField()
    roleName = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'loginId': self.loginId,
            'password': self.password,
            'confirmPassword': self.confirmPassword,
            'dob': self.dob.strftime('%Y-%m-%d'),
            'address': self.address,
            'gender': self.gender,
            'mobileNumber': self.mobileNumber,
            'roleId': self.roleId,
            'roleName': self.roleName
        }
        return data

    class Meta:
        db_table = 'sos_user'


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = 'sos_role'


class College(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)

    class Meta:
        db_table = 'sos_college'


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    class Meta:
        db_table = 'sos_course'


class Subject(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    courseId = models.IntegerField()
    courseName = models.CharField(max_length=50)

    class Meta:
        db_table = 'sos_subject'


class Faculty(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    collegeId = models.IntegerField()
    collegeName = models.CharField(max_length=50)
    subjectId = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    courseId = models.IntegerField()
    courseName = models.CharField(max_length=50)

    class Meta:
        db_table = 'sos_faculty'


class Marksheet(models.Model):
    rollNumber = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    physics = models.IntegerField()
    chemistry = models.IntegerField()
    maths = models.IntegerField()

    class Meta:
        db_table = 'sos_marksheet'


class Student(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    mobileNumber = models.CharField(max_length=20)
    email = models.EmailField()
    collegeId = models.IntegerField()
    collegeName = models.CharField(max_length=50)

    class Meta:
        db_table = 'sos_student'


class TimeTable(models.Model):
    examTime = models.CharField(max_length=40)
    examDate = models.DateField()
    subjectId = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    courseId = models.IntegerField()
    courseName = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)

    class Meta:
        db_table = 'sos_timetable'
