from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from app01 import models
from functools import wraps
from decimal import *


def success(result):
    return JsonResponse({
        'state': 'success',
        'result': result,
    })


def unsuccess(result):
    return JsonResponse({
        'state': 'unsuccess',
        'result': result,
    })


# Create your views here.
@csrf_exempt
def register(request):
    if request.method == "POST":
        studentName = request.POST.get("name")
        studentPassword1 = request.POST.get("password")
        studentEmail = request.POST.get("email")
        try:
            models.Student.objects.create(student_name=studentName, student_password=studentPassword1,
                                          student_email=studentEmail)
            return success('Register Success')
        except BaseException:
            return unsuccess('Username or Email already exists')
    return unsuccess('Request Method is not POST')


def check_login(f):
    @wraps(f)
    def inner(request, *args, **kwargs):
        if request.session.get("is_login") == "1":
            return f(request, *args, **kwargs)
        else:
            return redirect("/login/")

    return inner


@csrf_exempt
def login(request):
    print(request.method)
    if request.method == "POST":
        studentName = request.POST.get("name")
        studentPassword = request.POST.get("password")
        print(studentName)
        try:
            # before login reset all login_state
            models.Student.objects.update(login_state='0')
            student = models.Student.objects.filter(student_name=studentName, student_password=studentPassword)
            if student:
                # if login success, set login_stete='1'
                models.Student.objects.filter(student_name=studentName).update(login_state=1)
                # user session to save login_state, but it will be refreshed each time when use command line client application
                request.session["is_login"] = "1"
                request.session["studentid"] = student[0].student_id
                return success('Login Success')
            else:
                return unsuccess('Login Unsuccess, username or password error')
        except BaseException:
            return unsuccess('Login Exception')
    return unsuccess('Request Method is not POST')


def logout(request):
    try:
        student = models.Student.objects.filter(login_state=1)
        if student:
            # request.session.flush()
            models.Student.objects.filter(student_name=student[0].student_name).update(login_state=0)
            result = str(student[0].student_name + ', Logout Success')
            return success(result)
        else:
            return unsuccess('Logout Unsuccess')
    except BaseException:
        return unsuccess('Logout Exception')


class ListRecode(object):
    def __init__(self, moduleCode, moduleName, year, semester, professorId, professorName):
        self.moduleCode = moduleCode
        self.moduleName = moduleName
        self.year = year
        self.semester = semester
        self.professorId = professorId
        self.professorName = professorName


def list(request):
    teaching = models.Teaching.objects.filter().order_by('module_code')
    # teaching = teaching.order_by()
    teaching = teaching.order_by('academic_year')
    teaching = teaching.order_by('academic_semester')
    result2 = "{0:<10}".format("Code") + "{0:<35}".format("Name") + "{0:<10}".format("Year") + "{0:<15}".format(
        "Semester") + "{0:<35}".format("Taught by") + '\n'
    the_academic_year=''
    the_academic_semester = ''
    the_module_code = ''
    i=1
    for e in teaching:
        # print(e.teaching_id)
        m = models.Module.objects.filter(module_code=e.module_code)
        # print(m[0].module_code)
        p = models.Professor.objects.filter(professor_id=e.professor_id)
        # print(e.professor_id)
        # recode1 = ListRecode(m[0].module_code, m[0].module_name, e.academic_year, e.academic_semester,
        #                      p[0].professor_id, p[0].professor_name)

        if(i==1):
            result2 = result2 + "{0:<10}".format(m[0].module_code) + "{0:<35}".format(
                m[0].module_name) + "{0:<10}".format(
                str(e.academic_year)) + "{0:<15}".format(str(e.academic_semester)) + "{0:<15}".format(
                str('(' + p[0].professor_id + ') ' + p[0].professor_name))
            the_academic_year = str(e.academic_year)
            the_academic_semester = str(e.academic_semester)
            the_module_code = str(e.module_code)
        else:
            if(str(e.academic_year)==the_academic_year and str(e.academic_semester)==the_academic_semester and str(e.module_code)==the_module_code):
                result2 = result2+str('  (' + p[0].professor_id + ') ' + p[0].professor_name)
            else:
                result2 = result2 + '\n'
                result2 = result2 + "{0:<10}".format(m[0].module_code) + "{0:<35}".format(
                    m[0].module_name) + "{0:<10}".format(
                    str(e.academic_year)) + "{0:<15}".format(str(e.academic_semester)) + "{0:<15}".format(
                    str('(' + p[0].professor_id + ') ' + p[0].professor_name))
            the_academic_year=str(e.academic_year)
            the_academic_semester=str(e.academic_semester)
            the_module_code=str(e.module_code)
        i=i+1
    return HttpResponse(result2)


def view(request):
    # professor teaching rating
    try:
        allProfessor = models.Professor.objects.all()
        result = ''
        for a in allProfessor:
            allTeaching = models.Teaching.objects.filter(professor_id=a.professor_id)
            ratingSum = 0
            ratingCount = 0
            for b in allTeaching:
                allRating = models.Rating.objects.filter(teaching_id=b.teaching_id)
                for c in allRating:
                    ratingSum += c.rating
                    ratingCount += 1
            if (ratingCount == 0):
                print(a.professor_id + '   do not have rating')
                result = result + 'The rating of Professor ' + a.professor_id + ' ' + a.professor_name + ' is NULL' + '\n'
            else:
                aveRating = ratingSum / ratingCount
                resultRating = Decimal(aveRating).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                star = str(int(resultRating) * '*')
                print(a.professor_id + '   ' + str(resultRating))
                result = result + 'The rating of Professor ' + a.professor_id + ' ' + a.professor_name + ' is ' + str(
                    star) + '\n'

        return HttpResponse(result)
    except BaseException:
        return unsuccess("query View Exception")


@csrf_exempt
def average(request):
    if request.method == "POST":
        professorId = request.POST.get("professorid")
        moduleCode = request.POST.get("modulecode")
        try:
            teach1 = models.Teaching.objects.filter(professor_id=professorId, module_code=moduleCode)
            ratingSum = 0
            ratingCount = 0
            for e in teach1:
                r = models.Rating.objects.filter(teaching_id=e.teaching_id)  # 得到多个rating记录
                for a in r:  # 循环这个科目的rating
                    ratingSum += a.rating
                    ratingCount += 1
            aveRating = ratingSum / ratingCount
            # round
            outputRating = Decimal(aveRating).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            professorName = models.Professor.objects.get(professor_id=professorId).professor_name
            moduleName = models.Module.objects.get(module_code=moduleCode).module_name
            result = 'The rating of Professor ' + professorName + ' (' + professorId + ') in module ' \
                     + moduleName + ' (' + moduleCode + ')' + ' is ' + str(int(outputRating) * '*')
            return success(result)
        except BaseException:
            return unsuccess("Please makesure input Correct")
    return unsuccess("Request method error")


@csrf_exempt
def rate(request):
    if request.method == "POST":
        professorId = request.POST.get("professorid")
        moduleCode = request.POST.get("modulecode")
        year = request.POST.get("year")
        semester = request.POST.get("semester")
        rating = request.POST.get("rating")
        # check login first
        student = models.Student.objects.filter(login_state=1)
        if student:
            pass
        else:
            return unsuccess('Please login first and then rating')

        # check rating between 1-5
        if ((rating == str(1)) | (rating == str(2)) | (rating == str(3)) | (rating == str(4)) | (rating == str(5))):
            pass
        else:
            return unsuccess("Rating Input Error")

        try:
            teachingId = models.Teaching.objects.get(professor_id=professorId, module_code=moduleCode,
                                                     academic_year=year, academic_semester=semester)
            studentId = student[0].student_id
            # student1 = models.Student.objects.get(student_id=studentId)
            # check does already rate
            if (models.Rating.objects.filter(student_id=studentId, teaching_id=teachingId)):
                return unsuccess("You've already rate")
            else:
                models.Rating.objects.create(student_id=studentId, teaching_id=teachingId, rating=rating)
                return success("RATE SUCCESSFUL")
        except BaseException:
            return unsuccess("Please makesure input Correct")
    return unsuccess('Request method error')


@check_login
def index(request):
    # return render(request, "index.html")
    studentid = request.session.get("studentid")
    student = models.Student.objects.filter(student_id=studentid)
    if student:
        return render(request, "index.html", {"student": student[0]})
    else:
        return render(request, "index.html", {"student": "UNKNOW"})
