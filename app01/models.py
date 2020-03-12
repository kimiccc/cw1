from django.db import models

# Create your models here.
class Student(models.Model):
    class Meta:
        db_table='student'
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=48,null=False,unique=True)
    student_email = models.EmailField(max_length=48,null=False,unique=True)
    student_password=models.CharField(max_length=128,null=False)
    login_state=models.IntegerField(default=0)

    def __str__(self):  #unicode
        return str(self.student_id)

class Professor(models.Model):
    class Meta:
        db_table='professor'
    professor_id = models.CharField(primary_key=True,max_length=48)
    professor_name = models.CharField(max_length=48,null=False)
    professor_email = models.EmailField(max_length=48,unique=True,null=True) #reserve
    professor_password=models.CharField(max_length=128) #reserve

    def __str__(self):  #unicode
        return str(self.professor_id)

class Module(models.Model):
    class Meta:
        db_table='module'
    module_code = models.CharField(primary_key=True,max_length=48)
    module_name = models.CharField(max_length=48,null=False,unique=True)

    def __str__(self):  #unicode
        return str(self.module_code)

class Teaching(models.Model):
    class Meta:
        db_table='teaching'

    semester_choices = (
        (1, "1"),
        (2, "2"),
    )
    teaching_id = models.AutoField(primary_key=True)
    module_code = models.ForeignKey('Module',on_delete=models.CASCADE) #PROTECT  SET_NULL  CASCADE
    professor_id = models.ForeignKey('Professor',on_delete=models.CASCADE)
    academic_year=models.CharField(max_length=8,null=False)
    academic_semester=models.SmallIntegerField(choices=semester_choices)

    def __str__(self):  #unicode
        return str(self.teaching_id)

class Rating(models.Model):
    class Meta:
        db_table='rating'
    rating_id = models.AutoField(primary_key=True)
    teaching_id = models.ForeignKey('Teaching',on_delete=models.CASCADE)
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE)
    rating=models.IntegerField()

    def __str__(self):  #unicode
        return str(self.rating_id)