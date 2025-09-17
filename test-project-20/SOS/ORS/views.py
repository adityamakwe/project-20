from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session

from .ctl.RegistrationCtl import RegistrationCtl
from .ctl.LoginCtl import LoginCtl
from .ctl.WelcomeCtl import WelcomeCtl
from .ctl.UserCtl import UserCtl
from .ctl.UserListCtl import UserListCtl
from .ctl.RoleCtl import RoleCtl
from .ctl.RoleListCtl import RoleListCtl
from .ctl.CollegeCtl import CollegeCtl
from .ctl.CollegeListCtl import CollegeListCtl
from .ctl.CourseCtl import CourseCtl
from .ctl.CourseListCtl import CourseListCtl
from .ctl.SubjectCtl import SubjectCtl
from .ctl.SubjectListCtl import SubjectListCtl
from .ctl.FacultyCtl import FacultyCtl
from .ctl.FacultyListCtl import FacultyListCtl
from .ctl.MarksheetCtl import MarksheetCtl
from .ctl.MarksheetListCtl import MarksheetListCtl
from .ctl.MarksheetMeritListCtl import MarksheetMeritListCtl
from .ctl.StudentCtl import StudentCtl
from .ctl.StudentListCtl import StudentListCtl
from .ctl.TimeTableCtl import TimeTableCtl
from .ctl.TimeTableListCtl import TimeTableListCtl
from .ctl.ForgetPasswordCtl import ForgetPasswordCtl
from .ctl.ChangePasswordCtl import ChangePasswordCtl


@csrf_exempt
def action(request, page="", operation="", id=0):
    if page == "Logout":
        Session.objects.all().delete()
        request.session['user'] = None
        page = "Login"
        form = {}
        form['message']= "logout successfully"
        form['error'] = False
        return render(request, 'Login.html', {"form": form})

    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    res = ctlObj.execute(request, {"operation": operation, "id": id})
    return res



def index(request):
    res = render(request, 'Welcome.html')
    return res
