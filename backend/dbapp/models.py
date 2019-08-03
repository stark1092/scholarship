from django.db import models

# Create your models here.
class User(models.Model):
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    DEPARTMENT_CHOICES = (
        ('media', 'media'),
        ('cad', 'cad'),
        ('hi_perf', 'hi_perf'),
        ('ai', 'ai'),
        ('software', 'software'),
        ('network', 'network'),
        ('gix', 'gix'),
        ('cs_ma', 'cs_ma')
    )
    SPECIFIC_STUDENT_TYPE = (
        ('master', 'master'),
        ('doctor_straight', 'doctor_straight'),
        ('master_doctor', 'master_doctor'),
        ('doctor_normal', 'doctor_normal')
    )
    GRADE_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('above', 'above')
    )
    STUDENT_STATUS_CHOICES = (
        ('cst', 'cst'),
        ('shenzhen', 'shenzhen'),
        ('other', 'other')
    )
    POLITICAL_STATUS_CHOICES = (
        ('party', 'party'),
        ('pre_party', 'pre_party'),
        ('league', 'league'),
        ('general', 'general'),
        ('other', 'other')
    )
    ## basic user info
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=30)
    user_type = models.IntegerField(null=False, default=0)
    ## extended user info
    class_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    department = models.CharField(max_length=15, choices=DEPARTMENT_CHOICES)
    student_type = models.CharField(max_length=25, choices=SPECIFIC_STUDENT_TYPE)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    student_status = models.CharField(max_length=10, choices=STUDENT_STATUS_CHOICES)
    political_status = models.CharField(max_length=15, choices=POLITICAL_STATUS_CHOICES)
    ethnic_group = models.CharField(max_length=100)
    instructor = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    post_code = models.CharField(max_length=20)
    is_project_started = models.BooleanField()
    ## self-maintained info
    register_date = models.DateTimeField(auto_now_add=True)
    apply_id = models.IntegerField(default=0)
    apply_date = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)    

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=100)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField(max_length=1000)
    ip = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

class Notify(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    link = models.TextField(max_length=1000)

def LogAction(action, username, ip, details=''):
    Log.objects.create(action=action,username=username, details=details,ip=ip)
