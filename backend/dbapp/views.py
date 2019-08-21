from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from dbapp import models
import requests
import urllib
import urllib.parse
import json
from config import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.forms.models import model_to_dict
import uuid
import sys
import datetime
sys.path.append('../')

# utils start
sessionUser = {}  # token - username
userSession = {}  # username - token


def createToken(username):
    # remove token if already exists
    if(username in userSession.keys()):
        token = userSession[username]
        if(token is not None):
            sessionUser.pop(token, None)
    uid = uuid.uuid4()
    sessionUser[str(uid)] = {'username': username,
                        'create_time': datetime.datetime.now()}
    userSession[username] = str(uid)
    return uid


def updateToken(uid):
    if(uid in sessionUser.keys()):
        sessionUser[uid]['create_time'] = datetime.datetime.now()


def validateToken(uid, expire_time):
    # user does not have token
    if(uid not in sessionUser.keys()):
        return None
    # token expired, delete it
    elif((datetime.datetime.now() - sessionUser[uid]['create_time']) >= datetime.timedelta(seconds=expire_time)):
        userSession.pop(sessionUser[uid]['username'], None)
        sessionUser.pop(uid, None)
        return None
    else:
        return sessionUser[uid]['username']


def check_login(f):
    @wraps(f)
    def inner(req, *arg, **kwargs):
        try:
            data = json.loads(req.body)
        except:
            return JsonResponse({'status': -1, 'message': '非法请求'})
        if('username' in data.keys() and validateToken(data['token'], token_exp_time) == data['username']):
            updateToken(data['token'])
            return f(req, *arg, **kwargs)
        else:
            return JsonResponse({'status': -1, 'message': '用户未登录'})
    return inner

def check_teacher(f):
    @wraps(f)
    def inner(req, *arg, **kwargs):
        try:
            data = json.loads(req.body)
        except:
            return JsonResponse({'status': -1, 'message': '非法请求'})
        try:
            if('username' in data.keys() and validateToken(data['token'], token_exp_time) == data['username']):
                user = models.User.objects.get(username=data['username'])
                if(user.user_type == 1):
                    updateToken(data['token'])
                    return f(req, *arg, **kwargs)
                else:
                    return JsonResponse({'status': 1, 'message': '无操作权限'})
            else:
                return JsonResponse({'status': -1, 'message': '用户未登录'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': -1, 'message': '非法请求'})
    return inner


def check_admin(f):
    @wraps(f)
    def inner(req, *arg, **kwargs):
        try:
            data = json.loads(req.body)
        except:
            return JsonResponse({'status': -1, 'message': '非法请求'})
        try:
            if('username' in data.keys() and validateToken(data['token'], token_exp_time) == data['username']):
                user = models.User.objects.get(username=data['username'])
                if(user.user_type == 2):
                    updateToken(data['token'])
                    return f(req, *arg, **kwargs)
                else:
                    return JsonResponse({'status': 1, 'message': '无操作权限'})
            else:
                return JsonResponse({'status': -1, 'message': '用户未登录'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': -1, 'message': '非法请求'})
    return inner

def check_admin_teacher(f):
    @wraps(f)
    def inner(req, *arg, **kwargs):
        try:
            data = json.loads(req.body)
        except:
            return JsonResponse({'status': -1, 'message': '非法请求'})
        try:
            if('username' in data.keys() and validateToken(data['token'], token_exp_time) == data['username']):
                user = models.User.objects.get(username=data['username'])
                if(user.user_type == 1 or user.user_type == 2):
                    updateToken(data['token'])
                    return f(req, *arg, **kwargs)
                else:
                    return JsonResponse({'status': 1, 'message': '无操作权限'})
            else:
                return JsonResponse({'status': -1, 'message': '用户未登录'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': -1, 'message': '非法请求'})
    return inner

def getIpAddr(req):
    if 'HTTP_X_FORWARDED_FOR' in req.META.keys():
        return req.META['HTTP_X_FORWARDED_FOR']
    else:
        return req.META['REMOTE_ADDR']

"""
Example return data of this API
{'name': 'nickname', 'fullname': 'realname', 
'student_id': '', 'email': 'test@example.com', 
'student_type': 'bachelor', 
'research_lab': '', 
'year': 2017, 'class_number': x, 'mobile': '', 'groups': ['']}
"""
def getStudentInfo(token):
    res = requests.get(
        'https://stu.cs.tsinghua.edu.cn/api/v2/userinfo?access_token=' + token)
    return json.loads(res.text)
# utils end

# Create your views here.


def userlogin_stucs(req):
    if(req.method == 'GET'):
        data = {'response_type': 'code',
                'client_id': stucs_client_id,
                'redirect_uri': hostname + '/userlogin_stucs_cb',
                'scope': 'user',
                'state': 'thucs'}
        result = {'status': 0, 'url': 'https://stu.cs.tsinghua.edu.cn/api/v2/authorize?' +
                  urllib.parse.urlencode(data)}
        return JsonResponse(result)


@csrf_exempt
def userlogin_stucs_cb(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            code = data["code"]
            if not code:
                result['message'] = '授权失败'
                return JsonResponse(result)
            data = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': hostname + '/userlogin_stucs_cb',
                    'client_id': stucs_client_id,
                    'client_secret': stucs_client_secret}
            res = requests.post(
                'https://stu.cs.tsinghua.edu.cn/api/v2/access_token', data=data)
            res = json.loads(res.text)
            if(not res or not "access_token" in res):
                result['message'] = '授权失败'
                return JsonResponse(result)
            token = res['access_token']
            stu = getStudentInfo(token)
            if(not stu or not 'user' in stu):
                result['message'] = '授权失败'
                return JsonResponse(result)
            stu = stu['user']
            stu_info = {'username': stu['student_id'],
                        'name': stu['fullname'],
                        'mobile': stu['mobile'],
                        'email': stu['email'],
                        'student_id': stu['student_id'],
                        'is_project_started': False}
            ## Allow teachers to login via Accounts9
            if(stu['student_type'] == 'staff'):
                stu_info['user_type'] = 1
            try:
                user, created = models.User.objects.get_or_create(
                    student_id=stu['student_id'], defaults=stu_info)
                models.LogAction('login', user, getIpAddr(req))
                result['token'] = createToken(user.username)
                result['user_type'] = user.user_type
                result['status'] = 0
                result['name'] = user.name
                result['username'] = user.username
                return JsonResponse(result)
            except Exception as e:
                print(e)
                result['message'] = '服务器内部错误'
                return JsonResponse(result)
        except:
            return JsonResponse(result)


@csrf_exempt
def userlogin(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            print(data)
            user = models.User.objects.get(username=data['username'])
            if(user.user_type == 0):
                result['message'] = '登录失败，该用户禁止使用密码登录'
                models.LogAction('login_failure', user, getIpAddr(
                    req), 'User is not allowed to login via password')
                return JsonResponse(result)
            elif(user.password != data['password']):
                result['message'] = '用户名或密码错误'
                models.LogAction('login_failure', user,
                                 getIpAddr(req), 'Wrong password')
                return JsonResponse(result)
            else:
                models.LogAction('login', user, getIpAddr(req))
                result['token'] = createToken(user.username)
                result['user_type'] = user.user_type
                result['name'] = user.name
                result['username'] = user.username
                result['status'] = 0
                return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '登录失败'
            return JsonResponse(result)


@check_login
@csrf_exempt
def getPersonalInfo(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            res = models.User.objects.get(username=data['username'])
            models.LogAction('getPersonalInfo', res, getIpAddr(req))
            res = model_to_dict(res)
            res.pop('password') ## !important
            res.pop('user_id')
            result['status'] = 0
            result['data'] = res
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '服务器内部错误'
            return JsonResponse(result)

@check_login
@csrf_exempt
def changePersonalInfo(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            data['data']['last_modify'] = datetime.datetime.now()
            res = models.User.objects.filter(username=data['username']).update(**data['data'])
            result['status'] = 0
            models.LogAction('changePersonalInfo', models.User.objects.get(username=data['username']), getIpAddr(req))
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '服务器内部错误'
            return JsonResponse(result)

@check_login
@csrf_exempt
def getNotify(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        #testNotify()
        try:
            data = json.loads(req.body)
            notify = []
            notifies = models.Notify.objects.all()
            for each_notify in notifies:
                notify.append({'title' : each_notify.title,
                            'date' : each_notify.date,
                            'link' : each_notify.link})
            result['data'] = notify
            result['status'] = 0
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '服务器内部错误'
            return JsonResponse(result)

@check_login
@csrf_exempt
def filterAndSort(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        testApplicant()
        try:
            data = json.loads(req.body)
            filters = {}
            print(data)
            for key in data['data']:
                if key != '' and key != 'scholarship_name' and key != 'ordering':
                    filters[key] = data['data'][key]
            if not filters:
                students = models.User.objects.all()
            else:
                students = models.User.objects.filter(**filters)
            if data['data']['scholarship_name'] == '':
                 applicants = models.ApplyInfo.objects.filter(user_id__in = students)
            else:
                names = models.ApplyInfoSetting.objects.filter(scholarship_name = data['data']['scholarship_name'])
                applicants = models.ApplyInfo.objects.filter(apply_info_id__in = names, user_id__in = students)
            cnt = 0
            upload_info = []
            for applicant in applicants:
                upload_info.append(json.loads(applicant.json))
            if data['data']['ordering'] != '':
                upload_info = sorted(upload_info, key = lambda score:score[data['data']['ordering']], reverse = True)
            for seq in range(len(upload_info)):
                upload_info[seq]['seq'] = str(seq)
            result['applicant'] = upload_info
            result['status'] = 0
            print(result)
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '服务器内部错误'
            return JsonResponse(result)
#因为评分与json还没有很好的结合起来，因此暂时采用这种方法。以下代码为test

def testApplicant():
    models.User.objects.all().delete()
    user = models.User(username = 'jzt',
                        password = '123456',
                        name = '金子童',
                        student_id = 2015011739,
                        user_type = 0,
                        class_name = 'asdfg',
                        gender = 'male',
                        department = 'media',
                        student_type = 'master',
                        grade = '1',
                        student_status = 'cst',
                        political_status = 'party',
                        ethnic_group = 'asdf',
                        instructor = 'asdf',
                        email = '123456@qq.com',
                        mobile = '123432',
                        address = 'asdfdas',
                        post_code = '123456',
                        is_project_started = False)
    user.save()
    models.ApplyMaterialSetting.objects.all().delete()
    ms = models.ApplyMaterialSetting(
        alias = 'example',
        json = 'docx'
    )
    ms.save()
    models.ApplyScoreRuleSetting.objects.all().delete()
    rs = models.ApplyScoreRuleSetting(
        alias = 'example',
        json = '+1',
        apply_material_id = ms
    )
    rs.save()
    models.ApplyInfoSetting.objects.all().delete()
    ais = models.ApplyInfoSetting(
        scholarship_name = 's1',
        apply_score_rule_id = rs,
        apply_material_id = ms,
        can_apply = True
    )
    ais.save()
    models.ApplyInfo.objects.all().delete()
    ai = models.ApplyInfo(
        user_id = user,
        json = '{"student_num": "123456",\
                    "name": "金子童",\
                    "a_paper": "1",\
                    "b_paper": "2",\
                    "c_paper": "3",\
                    "o_paper": "4",\
                    "patent": "0",\
                    "academic_score": "5",\
                    "work_score": "5",\
                    "teacher_score": "5",\
                    "tot_score": "10",\
                    "num_report": "0",\
                    "link": {\
                        "link": "123456",\
                        "label": "点击查看"\
                    }\
                }',
        apply_info_id = ais,
        apply_score_rule_id = rs,
        apply_material_id = ms,
        score = 100,
        is_score_updated = True,
        is_user_confirm = True
    )
    ai.save()

def testNotify():
    models.Notify.objects.all().delete()
    for i in range(5):
        notify = models.Notify(title = 'test' + str(i),
                    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    link = 'link' + str(i))
        notify.save()
    models.Notify.objects.filter(title='test2').delete()

    @check_admin_teacher
@csrf_exempt
def changePassword(req):
    '''Allow user to change the pwd
    '''
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            user = models.User.objects.get(username=data['username'])
            old_pwd = data['data']['old_pwd']
            new_pwd = data['data']['new_pwd']
            if user.password == old_pwd:
                res = models.User.objects.filter(username=data['username']).update(password = new_pwd)
                result['status'] = 0
            else:
                result['message'] = '密码错误'
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '服务器内部错误'
            return JsonResponse(result)