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


def getIpAddr(req):
    if 'HTTP_X_FORWARDED_FOR' in req.META.keys():
        return req.META['HTTP_X_FORWARDED_FOR']
    else:
        return req.META['REMOTE_ADDR']


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
                        'is_admin': False,
                        'is_project_started': False}
            try:
                user, created = models.User.objects.get_or_create(
                    student_id=stu['student_id'], defaults=stu_info)
                models.LogAction('login', user, getIpAddr(req))
                result['token'] = createToken(user.username)
                result['is_admin'] = user.is_admin
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
            if(user.password == ''):
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
                result['is_admin'] = user.is_admin
                result['name'] = user.name
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
            res.pop('password')
            res.pop('id')
            res.pop('apply_id')
            res.pop('is_admin')
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
