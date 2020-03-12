from decimal import *
a=2.5
b=3.5
c=7.325
Decimal(str(c)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
print(round(a))
print(round(b))
print(Decimal(c).quantize(Decimal('.01'), rounding=ROUND_DOWN))

print(Decimal(str(3.3)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
print(Decimal(str(3.5)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
print(Decimal(3.74).quantize(Decimal('1.'), rounding=ROUND_HALF_UP))
print(Decimal(3.54).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
print(Decimal(3.45).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
print(type(Decimal(3.45).quantize(Decimal('1'), rounding=ROUND_HALF_UP)))
print(type(str(Decimal(3.45).quantize(Decimal('1'), rounding=ROUND_HALF_UP))))
from django.shortcuts import render, HttpResponse, redirect
import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from app01 import models
from functools import wraps
from decimal import *


# Create your views here.
@csrf_exempt
def register(request):
    if request.method == "POST":
        studentName = request.POST.get("name")
        studentPassword1 = request.POST.get("password1")
        # studentPassword2 = request.POST.get("password2")
        # if(studentPassword1==studentPassword1):
        #     print('11');
        # else:
        #     return render(request, "register.html")
        studentEmail = request.POST.get("email")
        models.Student.objects.create(student_name=studentName, student_password=studentPassword1,
                                      student_email=studentEmail)
        return HttpResponse("Request Success!")
    return render(request, "register.html")


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
    if request.method == "POST":
        studentName = request.POST.get("name")
        studentPassword = request.POST.get("password")
        student = models.Student.objects.filter(student_name=studentName, student_password=studentPassword)
        if student:
            # 登录成功
            request.session["is_login"] = "1"
            # 生成特殊字符串，当成key，在数据库的session表中对应一个session value
            # 写入coockie
            request.session["studentid"] = student[0].student_id
            # return redirect("/index/")
            return HttpResponse("Login Success")
        else:
            # return render(request, "login.html")
            return HttpResponse("Login NO Success")
    return HttpResponse("NO POSS")
    # return render(request, "login.html")


def logout(request):
    request.session.flush()
    return redirect("/index/")


class ListRecode(object):
    def __init__(self, moduleCode, moduleName, year, semester, professorId, professorName):
        self.moduleCode = moduleCode
        self.moduleName = moduleName
        self.year = year
        self.semester = semester
        self.professorId = professorId
        self.professorName = professorName


def list(request):
    teaching = models.Teaching.objects.all()
    rc = []
    for e in teaching:
        m = models.Module.objects.filter(module_code=e.module_code)
        print(m[0].module_code)
        p = models.Professor.objects.filter(professor_id=e.professor_id)
        print(e.professor_id)
        recode1 = ListRecode(m[0].module_code, m[0].module_name, e.academic_year, e.academic_semester,
                             p[0].professor_id, p[0].professor_name)
        print(recode1)
        rc.append(recode1.__dict__)
    i = 0
    for a in rc:
        print('rccccccc', a)
    print(json.dumps(rc))
    return HttpResponse(json.dumps(rc))


def view(request):
    # professor teaching rating
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
            result = result + "\n" + a.professor_id + '   do not have rating'
        else:
            aveRating = ratingSum / ratingCount
            resultRating = Decimal(aveRating).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            print(a.professor_id + '   ' + str(resultRating))
            result = result + '\n' + a.professor_id + '   ' + str(resultRating)

    return HttpResponse(result)


@csrf_exempt
def average(request):
    if request.method == "POST":
        professorId = request.POST.get("professorid")
        moduleCode = request.POST.get("modulecode")
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
                 + moduleName + ' (' + moduleCode + ')' + ' is ' + str(outputRating)
        print(result)
        return HttpResponse(result)
    return render(request, "average.html")


@csrf_exempt
@check_login  # Check if you are logged in, you can only rate after login
def rate(request):
    if request.method == "POST":
        professorId = request.POST.get("professorid")
        moduleCode = request.POST.get("modulecode")
        year = request.POST.get("year")
        semester = request.POST.get("semester")
        rating = request.POST.get("rating")
        # check rating between 1-5
        if ((rating == str(1)) | (rating == str(2)) | (rating == str(3)) | (rating == str(4)) | (rating == str(5))):
            print('Yes')
        else:
            print('NO')
            return render(request, "rate.html")
        teachingId = models.Teaching.objects.get(professor_id=professorId, module_code=moduleCode,
                                                 academic_year=year, academic_semester=semester)
        studentId = request.session.get("studentid")
        student1 = models.Student.objects.get(student_id=studentId)
        # check does already rate
        if (models.Rating.objects.filter(student_id=student1, teaching_id=teachingId)):
            print('EXIST')
            return HttpResponse("You've already rate")
        else:
            print('NO')
            models.Rating.objects.create(student_id=student1, teaching_id=teachingId, rating=rating)
            return HttpResponse("RATE SUCCESSFUL")
    return render(request, "rate.html")


@check_login
def index(request):
    # return render(request, "index.html")
    studentid = request.session.get("studentid")
    student = models.Student.objects.filter(student_id=studentid)
    if student:
        return render(request, "index.html", {"student": student[0]})
    else:
        return render(request, "index.html", {"student": "UNKNOW"})