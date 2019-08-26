"""scholarship URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dbapp import views

urlpatterns = [
    path('userlogin_stucs', views.userlogin_stucs),
    path('userlogin_stucs_cb', views.userlogin_stucs_cb),
    path('userlogin', views.userlogin),
    path('getPersonalInfo', views.getPersonalInfo),
    path('changePersonalInfo', views.changePersonalInfo),
    path('getNotify', views.getNotify),
    path('sendNotify', views.sendNotify),
    path('sendNotifyUpload', views.sendNotifyUpload),
    path('delNotify', views.delNotify),
    path('filterAndSort', views.filterAndSort),
    path('changePassword', views.changePassword),
    ### material APIs
    path('addMaterial', views.addMaterial),
    path('getMaterial', views.getMaterial),
    path('getMaterialList',views.getMaterialList),
    path('delMaterial', views.delMaterial),
    path('editMaterial', views.editMaterial),
    ### scoreRule APIs
    path('addScoreRule', views.addScoreRule),
    path('getScoreRule', views.getScoreRule),
    path('getScoreRuleList', views.getScoreRuleList),
    path('delScoreRule', views.delScoreRule),
    path('editScoreRule', views.editScoreRule),
    ### scholarshipInfo APIs
    path('addScholarshipInfo', views.addScholarshipInfo),
    path('getAvailableScholarshipList', views.getAvailableScholarshipList),
    path('getAllScholarshipList', views.getAllScholarshipList),
    path('getScholarshipMaterial', views.getScholarshipMaterial),
    path('getScholarshipInfoList', views.getScholarshipInfoList),
    path('delScholarshipInfo', views.delScholarshipInfo),
    path('editScholarshipInfo', views.editScholarshipInfo),
    path('switchScholarshipAvailability', views.switchScholarshipAvailability),
    ### application APIs
    path('sendApplyInfo', views.sendApplyInfo),
    path('obtainApplyInfo', views.obtainApplyInfo),
    path('withdrawApplyInfo', views.withdrawApplyInfo),
    ### teacher score APIs
    path('setApplyInfoScore', views.setApplyInfoScore),
    path('getApplyInfoScore', views.getApplyInfoScore)
]
