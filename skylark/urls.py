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
from application.testcase.views import TestCaseViewSets

router = routers.SimpleRouter(trailing_slash=False)
router.register('user/info', NormalUserViewSets, basename='user_info')
router.register('user/admin', AdminUserViewSets, basename='user')
router.register('user/group', GroupViewSets, basename='group')
router.register('keyword/lib-keyword', LibKeywordViewSets, basename='lib_keyword')
router.register('keyword/user-keyword', UserKeywordViewSets, basename='user_keyword')
router.register('test-case', TestCaseViewSets, basename='test_case')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    path(r'api/user/login', NoAuthUserViewSets.as_view({'post': 'login'})),
    path(r'api/user/reset', NoAuthUserViewSets.as_view({'post': 'reset'})),
]
