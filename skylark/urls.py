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
from django.conf import settings
from django.conf.urls import include, url
from django.views.static import serve
from rest_framework import routers
from application.user.views import NoAuthUserViewSets, AdminUserViewSets, NormalUserViewSets
from application.project.views import AdminProjectViewSets
from application.group.views import GroupViewSets
from application.libkeyword.views import LibKeywordViewSets
from application.userkeyword.views import UserKeywordViewSets
from application.caseentity.views import CaseEntityViewSets
from application.testcase.views import TestCaseViewSets
from application.testsuite.views import TestSuiteViewSets
from application.suitedir.views import SuiteDirViewSets
from application.project.views import ProjectViewSets
from application.setupteardown.views import SetupTeardownViewSets
from application.keywordgroup.views import KeywordGroupViewSets
from application.environment.views import EnvironmentViewSets
from application.variable.views import VariableViewSets
from application.builder.views import TestBuilderViewSets, DebugBuilderViewSets
from application.buildplan.views import BuildPlanViewSets
from application.buildhistory.views import BuildHistoryViewSets
from application.projectversion.views import ProjectVersionViewSets
from application.tag.views import TagViewSets
from application.casepriority.views import CasePriorityViewSets

router = routers.SimpleRouter(trailing_slash=False)
router.register('admin/user/info', AdminUserViewSets, basename='admin_uio')
router.register('admin/user/group', AdminUserViewSets, basename='admin_ugp')
router.register('admin/project', AdminProjectViewSets, basename='admin_project')
router.register('user/info', NormalUserViewSets, basename='user_info')
router.register('user/group', GroupViewSets, basename='user_group')
router.register('keyword/lib-keyword', LibKeywordViewSets, basename='lib_keyword')
router.register('keyword/user-keyword', UserKeywordViewSets, basename='user_keyword')
router.register('project', ProjectViewSets, basename='project')
router.register('suite-dir', SuiteDirViewSets, basename='suite_dir')
router.register('test-suite', TestSuiteViewSets, basename='test_suite')
router.register('test-case', TestCaseViewSets, basename='test_case')
router.register('case-entity', CaseEntityViewSets, basename='case_entity')
router.register('setup-teardown', SetupTeardownViewSets, basename='setup_teardown')
router.register('keyword-group', KeywordGroupViewSets, basename='keyword_group')
router.register('environment', EnvironmentViewSets, basename='environment')
router.register('variable', VariableViewSets, basename='variable')
router.register('project-version', ProjectVersionViewSets, basename='project_version')
router.register('build/test', TestBuilderViewSets, basename='build_test')
router.register('build/debug', DebugBuilderViewSets, basename='build_debug')
router.register('build/plan', BuildPlanViewSets, basename='build_plan')
router.register('build/history', BuildHistoryViewSets, basename='build_history')
router.register('tag', TagViewSets, basename='tag')
router.register('case-priority', CasePriorityViewSets, basename='case_priority')


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path(r'api/user/login', NoAuthUserViewSets.as_view({'post': 'login'})),
    path(r'api/user/register', NoAuthUserViewSets.as_view({'post': 'register'})),
    path(r'api/user/reset', NoAuthUserViewSets.as_view({'post': 'reset'})),
]
