"""skylark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from application.user.views import NoAuthUserViewSets, AdminUserViewSets, NormalUserViewSets
from application.group.views import GroupViewSets
from application.libkeyword.views import LibKeywordViewSets
from application.userkeyword.views import UserKeywordViewSets
from application.caseentity.views import CaseEntityViewSets
from application.testcase.views import TestCaseViewSets
from application.testsuite.views import TestSuiteViewSets
from application.suitedir.views import SuiteDirViewSets
from application.project.views import ProjectViewSets

router = routers.SimpleRouter(trailing_slash=False)
router.register('user/info', NormalUserViewSets, basename='user_info')
router.register('user/admin', AdminUserViewSets, basename='user')
router.register('user/group', GroupViewSets, basename='group')
router.register('keyword/lib-keyword', LibKeywordViewSets, basename='lib_keyword')
router.register('keyword/user-keyword', UserKeywordViewSets, basename='user_keyword')
router.register('case-entity', CaseEntityViewSets, basename='case_entity')
router.register('test-case', TestCaseViewSets, basename='test_case')
router.register('test-suite', TestSuiteViewSets, basename='test_suite')
router.register('suite-dir', SuiteDirViewSets, basename='suite_dir')
router.register('project', ProjectViewSets, basename='project')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    path(r'api/user/login', NoAuthUserViewSets.as_view({'post': 'login'})),
    path(r'api/user/reset', NoAuthUserViewSets.as_view({'post': 'reset'})),
]
