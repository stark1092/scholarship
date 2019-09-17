from functools import wraps
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.core.paginator import Paginator
from dbapp import models
import requests
import urllib
from django.utils.timezone import utc
import urllib.parse
import json
from config import *
import uuid
import sys
import datetime
import mammoth
from dbapp import scorer
import time
import xlwt
from io import BytesIO
sys.path.append('../')

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

scorer_executor = ThreadPoolExecutor(max_workers=scorer_workers)
scorer_map = {}

def scorerInBackGround(*arg, **kwargs):
    user_id = kwargs['user']
    apply_info_id = kwargs['apply_info']
    print("Start scoring user:{}, apply:{}...".format(user_id, apply_info_id))
    time.sleep(0.1)
    try:
        user = models.User.objects.get(user_id=user_id)
        apply_info = models.ApplyInfoSetting.objects.get(apply_info_id=apply_info_id)
        entry = models.ApplyInfo.objects.get(user_id=user,apply_info_id=apply_info)
        if(apply_info.apply_score_rule_id.apply_score_rule_id not in scorer_map):
            scorer_map[apply_info.apply_score_rule_id.apply_score_rule_id] = scorer.ScoreCalculator(json.loads(apply_info.apply_score_rule_id.json))
        print("Get entry succesfully, evaluating...")
        score_res = scorer_map[apply_info.apply_score_rule_id.apply_score_rule_id].getScore(json.loads(entry.json), entry.extra_score)
        entry.score = score_res[0]
        entry.academic_score = score_res[1]
        entry.work_score = score_res[2]
        entry.extra_info = json.dumps(score_res[3])
        entry.wrong_time = score_res[4]
        entry.is_score_updated = True
        entry.save()
        print(score_res)
    except Exception as e:
        print(e)
    finally:
        connections.close_all()

# utils start

def createToken(user):
    # update token if already exists
    token = str(uuid.uuid4())
    models.SessionToken.objects.update_or_create(user=user, 
        defaults={'user': user, 'token': token, 'set_time': datetime.datetime.utcnow().replace(tzinfo=utc)})
    return token


def updateToken(user):
    try:
        obj = models.SessionToken.objects.get(user=user)
        obj.set_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        obj.save(force_update=True)
    except Exception as e:
        print(e)

def getToken(user, expire_time):
    try:
        obj = models.SessionToken.objects.get(user=user)
        if(datetime.datetime.utcnow().replace(tzinfo=utc) - obj.set_time >= datetime.timedelta(seconds=expire_time)):
            return ''
        else:
            return obj.token
    except Exception as e:
        print(e)
        return ''

def check_login(f):
    @wraps(f)
    def inner(req, *arg, **kwargs):
        try:
            data = json.loads(req.body)
            if('username' in data.keys() and 'token' in data.keys()):
                pass
            else:
                raise Exception()
        except:
            return JsonResponse({'status': -1, 'message': '非法请求'})
        try:
            user = models.User.objects.get(username=data['username'])
            token = getToken(user, token_exp_time)
            if(token == data['token']):
                updateToken(user)
                return f(req, *arg, **kwargs)
            else:
                return JsonResponse({'status': -1, 'message': '用户未登录'})
        except:
            return JsonResponse({'status': -1, 'message': '非法请求'})
    return inner


def check_teacher(f):
    @wraps(f)
    def inner(req, *arg, **kwargs):
        try:
            data = json.loads(req.body)
            if('username' in data.keys() and 'token' in data.keys()):
                pass
            else:
                raise Exception()
        except:
            return JsonResponse({'status': -1, 'message': '非法请求'})
        try:
            user = models.User.objects.get(username=data['username'])
            token = getToken(user, token_exp_time)
            if(token == data['token'] and user.user_type == 1):
                updateToken(user)
                return f(req, *arg, **kwargs)
            else:
                return JsonResponse({'status': -1, 'message': '用户未登录'})
        except:
            return JsonResponse({'status': -1, 'message': '非法请求'})
    return inner


def check_admin(f):
    @wraps(f)
    def inner(req, *arg, **kwargs):
        try:
            data = json.loads(req.body)
            if('username' in data.keys() and 'token' in data.keys()):
                pass
            else:
                raise Exception()
        except:
            return JsonResponse({'status': -1, 'message': '非法请求'})
        try:
            user = models.User.objects.get(username=data['username'])
            token = getToken(user, token_exp_time)
            if(token == data['token'] and user.user_type == 2):
                updateToken(user)
                return f(req, *arg, **kwargs)
            else:
                return JsonResponse({'status': -1, 'message': '用户未登录'})
        except:
            return JsonResponse({'status': -1, 'message': '非法请求'})
    return inner


def check_admin_teacher(f):
    @wraps(f)
    def inner(req, *arg, **kwargs):
        try:
            data = json.loads(req.body)
            if('username' in data.keys() and 'token' in data.keys()):
                pass
            else:
                raise Exception()
        except:
            return JsonResponse({'status': -1, 'message': '非法请求'})
        try:
            user = models.User.objects.get(username=data['username'])
            token = getToken(user, token_exp_time)
            if(token == data['token'] and (user.user_type == 1 or user.user_type == 2)):
                updateToken(user)
                return f(req, *arg, **kwargs)
            else:
                return JsonResponse({'status': -1, 'message': '用户未登录'})
        except:
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
            # Allow teachers to login via Accounts9
            if(stu['student_type'] == 'staff'):
                stu_info['user_type'] = 1
            try:
                user, created = models.User.objects.get_or_create(
                    student_id=stu['student_id'], defaults=stu_info)
                models.LogAction('login', user, getIpAddr(req))
                ## in some cases, OAuth API may return empty name
                if(user.name == ''):
                    user.name = stu['fullname']
                    user.save(force_update=True)
                result['token'] = createToken(user)
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
            user = models.User.objects.get(username=data['username'])
            if(user.user_type == 0 or user.password == ""):
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
                result['token'] = createToken(user)
                result['user_type'] = user.user_type
                result['status'] = 0
                result['name'] = user.name
                result['username'] = user.username
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
            res = None
            if('stu_num' in data.keys()):
                res = models.User.objects.get(student_id=data['stu_num'])
            else:
                res = models.User.objects.get(username=data['username'])
            res = model_to_dict(res)
            res.pop('password')  # !important
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
            data['data']['last_modify'] = datetime.datetime.utcnow().replace(tzinfo=utc)
            res = models.User.objects.filter(
                username=data['username']).update(**data['data'])
            result['status'] = 0
            models.LogAction('changePersonalInfo', models.User.objects.get(
                username=data['username']), getIpAddr(req))
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
        try:
            data = json.loads(req.body)
            notify = []
            notifies = models.Notify.objects.all().order_by('-date')
            for each_notify in notifies:
                notify.append({'title': each_notify.title,
                               'date': each_notify.date,
                               'link': each_notify.link,
                               'id': each_notify.id})
            result['data'] = notify
            result['status'] = 0
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '服务器内部错误'
            return JsonResponse(result)


@check_admin
@csrf_exempt
def delNotify(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            models.Notify.objects.filter(
                id=data['data']['id'], title=data['data']['title']).delete()
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '服务器内部错误'
        finally:
            return JsonResponse(result)


@check_admin
@csrf_exempt
def sendNotify(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            models.Notify.objects.create(
                title=data['data']['title'], link=data['data']['link'])
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '服务器内部错误'
        finally:
            return JsonResponse(result)


@csrf_exempt
def sendNotifyUpload(req):
    if(req.method == 'POST'):
        try:
            result = {'status': 1}
            username = req.POST.get('username')
            token = req.POST.get('token')
            f = req.FILES.get('file')
            title = req.POST.get('title')
            user = models.User.objects.get(username=username)
            if(token == getToken(user, token_exp_time)):
                if(user.user_type == 2):
                    updateToken(user)
                    # do real work here
                    f.seek(0)
                    converted = mammoth.convert_to_html(f)
                    html = converted.value
                    models.Notify.objects.create(
                        title=title, link=converted.value)
                    result['status'] = 0
                else:
                    result['message'] = '无操作权限'
            else:
                result['status'] = -1
                result['message'] = '用户未登录'
        except Exception as e:
            print(e)
            result['message'] = '请求无效'
        finally:
            return JsonResponse(result)


@check_login
@csrf_exempt
def filterAndSort(req):
    if(req.method == 'POST'):
        result = { 'status' : 1 }
        try:
            data = json.loads(req.body)
            data = data['data']
            ordering = None
            if(data['ordering'] == 'tot_score'):
                ordering = "-score"
            elif(data['ordering'] == 'academic_score'):
                ordering = "-academic_score"
            elif(data['ordering'] == 'work_score'):
                ordering = "-work_score"
            filter = {}
            filter['apply_info_id'] = data['scholarship_name']
            if(data['department'] != ''):
                filter['user_id__department'] = data['department']
            if(data['student_type'] == 'master'):
                filter['user_id__student_type'] = 'master'
            else:
                filter['user_id__student_type__in'] = ['doctor_straight', 'master_doctor', 'doctor_normal']
            queries = models.ApplyInfo.objects.filter(**filter, is_score_updated=False, is_user_confirm=True)
            for entry in queries.iterator():
                try:
                    print("Found entries not evaluated, start evaluating...")
                    scorer_id = entry.apply_info_id.apply_score_rule_id.apply_score_rule_id
                    if(scorer_id not in scorer_map):
                        scorer_map[scorer_id] = scorer.ScoreCalculator(json.loads(entry.apply_info_id.apply_score_rule_id.json))
                    score_res = scorer_map[scorer_id].getScore(json.loads(entry.json), entry.extra_score)
                    entry.score = score_res[0]
                    entry.academic_score = score_res[1]
                    entry.work_score = score_res[2]
                    entry.extra_info = json.dumps(score_res[3])
                    entry.wrong_time = score_res[4]
                    entry.is_score_updated = True
                    entry.save()
                    print(score_res)
                except Exception as e:
                    print(e)
            ## return results
            queries = models.ApplyInfo.objects.filter(**filter, is_score_updated=True, is_user_confirm=True).order_by(ordering, "user_id_id")
            pages = Paginator(queries, 15)
            page = pages.page(data['page'])
            result['data'] = { 'page_cnt': pages.num_pages, 'count': pages.count, 'curr_entries': [] }
            seq = (data['page'] - 1) * 15
            for item in page.object_list:
                entry = {'seq': seq, 'student_num': item.user_id.student_id, 'name': item.user_id.name, 
                'academic_score': item.academic_score, 'work_score': item.work_score, 'tot_score': item.score,
                'num_report': item.report_num }
                seq += 1
                ## merge A,B,C,O and patent nums
                if(item.extra_info != ""):
                    try:
                        extras = json.loads(item.extra_info)
                        if('academic' in extras.keys()):
                            extras = extras['academic']
                            patent_cnt = 0
                            paper_cnt = {'A-1': 0, 'B-1': 0, 'C-1': 0, 'O-1': 0}
                            if('conf_paper' in extras.keys() and isinstance(extras['conf_paper'], dict)):
                                for k in extras['conf_paper'].keys():
                                    paper_cnt[k] += extras['conf_paper'][k]
                            if('journal_paper' in extras.keys() and isinstance(extras['journal_paper'], dict)):
                                for k in extras['journal_paper'].keys():
                                    paper_cnt[k] += extras['journal_paper'][k]
                            if('patent' in extras.keys() and not isinstance(extras['patent'], dict)):
                                patent_cnt += extras['patent']
                        entry['patent'] = patent_cnt
                        entry['a_paper'] = paper_cnt['A-1']
                        entry['b_paper'] = paper_cnt['B-1']
                        entry['c_paper'] = paper_cnt['C-1']
                        entry['o_paper'] = paper_cnt['O-1']
                    except Exception as e:
                        print(e)
                result['data']['curr_entries'].append(entry)
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '服务器内部错误'
        finally:
            return JsonResponse(result)

@check_admin
@csrf_exempt
def exportExcel(req):
    if(req.method == 'POST'):
        result = { 'status' : 1 }
        try:
            data = json.loads(req.body)
            data = data['data']
            ordering = None
            if(data['ordering'] == 'tot_score'):
                ordering = "-score"
            elif(data['ordering'] == 'academic_score'):
                ordering = "-academic_score"
            elif(data['ordering'] == 'work_score'):
                ordering = "-work_score"
            filter = {}
            filter['apply_info_id'] = data['scholarship_name']
            if(data['department'] != ''):
                filter['user_id__department'] = data['department']
            if(data['student_type'] == 'master'):
                filter['user_id__student_type'] = 'master'
            else:
                filter['user_id__student_type__in'] = ['doctor_straight', 'master_doctor', 'doctor_normal']
            queries = models.ApplyInfo.objects.filter(**filter, is_score_updated=False, is_user_confirm=True)
            for entry in queries.iterator():
                try:
                    print("Found entries not evaluated, start evaluating...")
                    scorer_id = entry.apply_info_id.apply_score_rule_id.apply_score_rule_id
                    if(scorer_id not in scorer_map):
                        scorer_map[scorer_id] = scorer.ScoreCalculator(json.loads(entry.apply_info_id.apply_score_rule_id.json))
                    score_res = scorer_map[scorer_id].getScore(json.loads(entry.json), entry.extra_score)
                    entry.score = score_res[0]
                    entry.academic_score = score_res[1]
                    entry.work_score = score_res[2]
                    entry.extra_info = json.dumps(score_res[3])
                    entry.wrong_time = score_res[4]
                    entry.is_score_updated = True
                    entry.save()
                    print(score_res)
                except Exception as e:
                    print(e)
            ## return results
            queries = models.ApplyInfo.objects.filter(**filter, is_score_updated=True, is_user_confirm=True).order_by(ordering, "user_id_id")
            
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename=order.xls'
            wb = xlwt.Workbook(encoding='utf8')
            sheet = wb.add_sheet('order-sheet')

            sheet.write(0,0,'编号')
            sheet.write(0,1,'学号')
            sheet.write(0,2,'姓名')
            sheet.write(0,3,'A类论文')
            sheet.write(0,4,'B类论文')
            sheet.write(0,5,'C类论文')
            sheet.write(0,6,'O类论文')
            sheet.write(0,7,'专利')
            sheet.write(0,8,'学术得分')
            sheet.write(0,9,'社工得分')
            sheet.write(0,10,'教师评分')
            sheet.write(0,11,'总分')
            sheet.write(0,12,'被举报数')

            seq = 0
            for item in queries:
                seq += 1
                sheet.write(seq, 0, seq)
                sheet.write(seq, 1, item.user_id.student_id)
                sheet.write(seq, 2, item.user_id.name)
                
                sheet.write(seq, 8, item.academic_score)
                sheet.write(seq, 9, item.work_score)
                sheet.write(seq, 10, 0)
                sheet.write(seq, 11, item.score)
                sheet.write(seq, 12, item.report_num)

                entry = {'patent': 0, 'a_paper': 0, 'b_paper': 0, 'c_paper': 0, 'o_paper': 0}
                if(item.extra_info != ""):
                    try:
                        extras = json.loads(item.extra_info)
                        if('academic' in extras.keys()):
                            extras = extras['academic']
                            patent_cnt = 0
                            paper_cnt = {'A-1': 0, 'B-1': 0, 'C-1': 0, 'O-1': 0}
                            if('conf_paper' in extras.keys() and isinstance(extras['conf_paper'], dict)):
                                for k in extras['conf_paper'].keys():
                                    paper_cnt[k] += extras['conf_paper'][k]
                            if('journal_paper' in extras.keys() and isinstance(extras['journal_paper'], dict)):
                                for k in extras['journal_paper'].keys():
                                    paper_cnt[k] += extras['journal_paper'][k]
                            if('patent' in extras.keys() and not isinstance(extras['patent'], dict)):
                                patent_cnt += extras['patent']
                        entry['patent'] = patent_cnt
                        entry['a_paper'] = paper_cnt['A-1']
                        entry['b_paper'] = paper_cnt['B-1']
                        entry['c_paper'] = paper_cnt['C-1']
                        entry['o_paper'] = paper_cnt['O-1']
                        
                    except Exception as e:
                        print(e)

                sheet.write(seq, 3, entry['a_paper'])
                sheet.write(seq, 4, entry['b_paper'])
                sheet.write(seq, 5, entry['c_paper'])
                sheet.write(seq, 6, entry['o_paper'])
                sheet.write(seq, 7, entry['patent'])

            
            sheet2 = wb.add_sheet('detail-sheet')

            sheet2.write(0,0,'编号')
            sheet2.write(0,1,'学号')
            sheet2.write(0,2,'姓名')
            sheet2.write(0,3,'学术成果')
            sheet2.write(0,4,'社会工作')
            sheet2.write(0,5,'其它学术')

            seq = 0
            for item in queries:
                seq += 1
                sheet2.write(seq, 0, seq)
                sheet2.write(seq, 1, item.user_id.student_id)
                sheet2.write(seq, 2, item.user_id.name)
                
                if(item.json != ""):
                    try:
                        # print("Not Empty")
                        academic_num = 0
                        details = json.loads(item.json)
                        if('academic' in details.keys()):
                            # print("academic")
                            adademics = details['academic']
                            # print(extras)
                            if('conf_paper' in adademics.keys()) :
                                for paper in adademics['conf_paper']:
                                    #print(paper)
                                    sheet2.write(seq+academic_num,3,str(paper))
                                    #print(paper)
                                    academic_num += 1
                            if('journal_paper' in adademics.keys()) :
                                for paper in adademics['journal_paper']:
                                    sheet2.write(seq+academic_num,3,str(paper))
                                    academic_num += 1
                            if('patent' in adademics.keys()) :
                                for paper in adademics['patent']:
                                    sheet2.write(seq+academic_num,3,str(paper))
                                    academic_num += 1
                            if('project' in adademics.keys()) :
                                for project in adademics['project']:
                                    sheet2.write(seq+academic_num,3,str(project))
                                    academic_num += 1
                            if('intl_standard' in adademics.keys()) :
                                for standard in adademics['intl_standard']:
                                    sheet2.write(seq+academic_num,3,str(standard))
                                    academic_num += 1
                            if('conf_award' in adademics.keys()) :
                                for award in adademics['conf_award']:
                                    sheet2.write(seq+academic_num,3,str(award))
                                    academic_num += 1      

                        work_num = 0
                        if('work' in details.keys()):
                            # print("academic")
                            works = details['work']
                            if('post' in works.keys()) :
                                for work in works['post']:
                                    sheet2.write(seq+work_num,4,str(work))
                                    work_num += 1
                            if('accu_pro' in works.keys()) :
                                for work in works['accu_pro']:
                                    sheet2.write(seq+work_num,4,str(work))
                                    work_num += 1

                        other_num = 0
                        if('other_academic' in details.keys()):
                            # print("academic")
                            other_num += 1
                            sheet2.write(seq,5,str(details['other_academic']))
                        seq+=max(academic_num,work_num,other_num)
                        
                    except Exception as e:
                        print(e)
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            response.write(output.getvalue())
            # response['status'] = 0
            return response
        except Exception as e:
            print(e)
            result['message'] = '服务器内部错误'
            return JsonResponse(result)


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
                user.password = new_pwd
                user.save()
                models.LogAction('changePassword', user, getIpAddr(req))
                result['status'] = 0
            else:
                result['message'] = '密码错误'
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '服务器内部错误'
            return JsonResponse(result)


#####
# Material APIs
#####

@check_admin
@csrf_exempt
def addMaterial(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            data = data['data']
            ms = models.ApplyMaterialSetting(
                alias=data['alias'],
                json=data['json']
            )
            ms.save()
            result['status'] = 0
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
            return JsonResponse(result)


@check_admin
@csrf_exempt
def getMaterial(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            result['data'] = models.ApplyMaterialSetting.objects.get(
                apply_material_id=data['data']).json
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
        finally:
            return JsonResponse(result)


@check_admin
@csrf_exempt
def getMaterialList(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            result['data'] = serializers.serialize('json', models.ApplyMaterialSetting.objects.all(
            ).order_by("-set_time"), fields=('apply_material_id', 'alias', 'set_time'))
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
        finally:
            return JsonResponse(result)


@check_admin
@csrf_exempt
def delMaterial(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            models.ApplyMaterialSetting.objects.filter(
                apply_material_id=data['data']).delete()
            result['status'] = 0
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
            return JsonResponse(result)


@check_admin
@csrf_exempt
def editMaterial(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            data = data['data']
            model = models.ApplyMaterialSetting.objects.get(
                apply_material_id=data['pk'])
            model.alias = data['alias']
            model.json = data['json']
            model.save(force_update=True)
            result['status'] = 0
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
            return JsonResponse(result)

#####
# ScoreRule APIs
#####


@check_admin
@csrf_exempt
def addScoreRule(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            data = data['data']
            ms = models.ApplyMaterialSetting.objects.get(
                apply_material_id=data['apply_material_id'])
            srs = models.ApplyScoreRuleSetting(
                alias=data['alias'],
                json=data['json'],
                apply_material_id=ms
            )
            srs.save()
            result['status'] = 0
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
            return JsonResponse(result)


@check_admin
@csrf_exempt
def getScoreRule(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            result['data'] = models.ApplyScoreRuleSetting.objects.get(
                apply_score_rule_id=data['data']).json
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
        finally:
            return JsonResponse(result)


@check_admin
@csrf_exempt
def getScoreRuleList(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            result['data'] = serializers.serialize('json', models.ApplyScoreRuleSetting.objects.all().order_by(
                "-set_time"), fields=('apply_score_rule_id', 'alias', 'set_time', 'apply_material_id'))
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
        finally:
            return JsonResponse(result)


@check_admin
@csrf_exempt
def delScoreRule(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            models.ApplyScoreRuleSetting.objects.filter(
                apply_score_rule_id=data['data']).delete()
            result['status'] = 0
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
            return JsonResponse(result)


@check_admin
@csrf_exempt
def editScoreRule(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            data = data['data']
            ms = models.ApplyMaterialSetting.objects.get(
                apply_material_id=data['apply_material_id'])
            model = models.ApplyScoreRuleSetting.objects.get(
                apply_score_rule_id=data['pk'])
            model.apply_material_id = ms
            model.alias = data['alias']
            model.json = data['json']
            model.save(force_update=True)
            ### refresh scorer if already in memory
            ### TODO - refresh user application entries
            if(data['pk'] in scorer_map.keys()):
                scorer_map[data['pk']] = scorer.ScoreCalculator(json.loads(data['json']))
            result['status'] = 0
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
            return JsonResponse(result)

#####
# Scholarship APIs
#####


@check_admin
@csrf_exempt
def addScholarshipInfo(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            data = data['data']
            srs = models.ApplyScoreRuleSetting.objects.get(
                apply_score_rule_id=data['score_rule'])
            models.ApplyInfoSetting.objects.create(
                scholarship_name=data['scholarship_name'],
                apply_score_rule_id=srs,
                can_apply=False,
            )
            result['status'] = 0
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
            return JsonResponse(result)


@check_login
@csrf_exempt
def getAvailableScholarshipList(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            result['data'] = serializers.serialize('json', models.ApplyInfoSetting.objects.filter(can_apply=True).order_by(
                "-set_time"), fields=('scholarship_name', 'apply_info_id', 'set_time', 'apply_score_rule_id'))
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
        finally:
            return JsonResponse(result)

@check_login
@csrf_exempt
def getAllScholarshipList(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            result['data'] = serializers.serialize('json', models.ApplyInfoSetting.objects.all().order_by(
                "-set_time"), fields=('scholarship_name', 'apply_info_id', 'set_time', 'apply_score_rule_id', 'can_apply'))
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
        finally:
            return JsonResponse(result)

@check_login
@csrf_exempt
def getScholarshipMaterial(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            result['data'] = models.ApplyInfoSetting.objects.get(
                apply_info_id=data['data']).apply_score_rule_id.apply_material_id.json
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
        finally:
            return JsonResponse(result)


@check_admin
@csrf_exempt
def getScholarshipInfoList(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            result['data'] = serializers.serialize(
                'json', models.ApplyInfoSetting.objects.all().order_by("-set_time"))
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
        finally:
            return JsonResponse(result)


@check_admin
@csrf_exempt
def delScholarshipInfo(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            models.ApplyInfoSetting.objects.filter(
                apply_info_id=data['data']).delete()
            result['status'] = 0
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
            return JsonResponse(result)


@check_admin
@csrf_exempt
def editScholarshipInfo(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            data = data['data']
            srs = models.ApplyScoreRuleSetting.objects.get(
                apply_score_rule_id=data['score_rule'])
            model = models.ApplyInfoSetting.objects.get(
                apply_info_id=data['pk'])
            model.apply_score_rule_id = srs
            model.scholarship_name = data['scholarship_name']
            model.save(force_update=True)
            result['status'] = 0
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
            return JsonResponse(result)


@check_admin
@csrf_exempt
def switchScholarshipAvailability(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            data = data['data']
            model = models.ApplyInfoSetting.objects.get(
                apply_info_id=data['pk'])
            model.can_apply = data['can_apply']
            model.save(force_update=True)
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = '操作失败'
        finally:
            return JsonResponse(result)

###
# Application APIs
###
@check_login
@csrf_exempt
def sendApplyInfo(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            model = models.ApplyInfoSetting.objects.get(
                apply_info_id=data['data']['scholarship_id'])
            user = models.User.objects.get(username=data['username'])
            models.ApplyInfo.objects.update_or_create(user_id=user, apply_info_id=model,
                                                      defaults={'apply_date': datetime.datetime.utcnow().replace(tzinfo=utc),
                                                                'score': 0,
                                                                'user_id': user,
                                                                'apply_info_id': model,
                                                                'json': data['data']['form'],
                                                                'is_score_updated': False,
                                                                'is_user_confirm': data['data']['confirm']})
            if(data['data']['confirm']):
                scorer_executor.submit(scorerInBackGround, user=user.user_id, apply_info=model.apply_info_id)
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = "申请时发生错误"
        finally:
            return JsonResponse(result)

@check_login
@csrf_exempt
def obtainApplyInfo(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            model = models.ApplyInfoSetting.objects.get(
                apply_info_id=data['data']['scholarship_id'])
            user = None
            if('stu_num' in data['data'].keys()):
                user = models.User.objects.get(student_id=data['data']['stu_num'])
            else:
                user = models.User.objects.get(username=data['username'])
            try:
                res = models.ApplyInfo.objects.get(user_id=user, apply_info_id=model)
                result['data'] = { 'json': res.json, 'is_user_confirm': res.is_user_confirm, 'id': res.apply_id }
            except models.ApplyInfo.DoesNotExist:
                result['data'] = ""
            finally:
                result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = "服务器内部错误"
        finally:
            return JsonResponse(result)

@check_login
@csrf_exempt
def withdrawApplyInfo(req):
    if(req.method == 'POST'):
        result = {'status': 1}
        try:
            data = json.loads(req.body)
            model = models.ApplyInfoSetting.objects.get(
                apply_info_id=data['data']['scholarship_id'])
            user = models.User.objects.get(username=data['username'])
            models.ApplyInfo.objects.filter(user_id=user, apply_info_id=model).delete()
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = "服务器内部错误"
        finally:
            return JsonResponse(result)

###
### Teacher Scoring
###
@check_teacher
@csrf_exempt
def setApplyInfoScore(req):
    if(req.method == 'POST'):
        result = {'status' : 1}
        try:
            data = json.loads(req.body)
            apply = models.ApplyInfo.objects.get(apply_id=data['data']['apply_id'])
            teacher = models.User.objects.get(username=data['username'])
            models.TeacherScore.objects.update_or_create(apply_id=apply, teacher_id=teacher, defaults={
                'teacher_id': teacher,
                'apply_id': apply,
                'score': data['data']['score']
            })
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = "服务器内部错误"
        finally:
            return JsonResponse(result)

@check_teacher
@csrf_exempt
def getApplyInfoScore(req):
    if(req.method == 'POST'):
        result = {'status' : 1}
        try:
            data = json.loads(req.body)
            apply = models.ApplyInfo.objects.get(apply_id=data['data']['apply_id'])
            teacher = models.User.objects.get(username=data['username'])
            try:
                res = models.TeacherScore.objects.get(apply_id=apply, teacher_id=teacher)
                result['data'] = res.score
            except models.TeacherScore.DoesNotExist:
                result['data'] = 0.0
            result['status'] = 0
        except Exception as e:
            print(e)
            result['message'] = "服务器内部错误"
        finally:
            return JsonResponse(result)
