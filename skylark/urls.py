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
from skylark.admin.urls import admin_router
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.views.static import serve
from rest_framework import routers
from application.user.views import NoAuthUserViewSets, NormalUserViewSets
from application.usergroup.views import UserGroupViewSets
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
from application.region.views import RegionViewSets
from application.variable.views import VariableViewSets
from application.builder.views import BuilderViewSets
from application.buildplan.views import BuildPlanViewSets
from application.buildrecord.views import BuildRecordViewSets
from application.buildhistory.views import BuildHistoryViewSets
from application.projectversion.views import ProjectVersionViewSets
from application.tag.views import TagViewSets
from application.casepriority.views import CasePriorityViewSets
from application.virtualfile.views import VirtualFileViewSets, ProjectFileViewSets, InternalFileViewSets
from application.notice.views import NoticeViewSets
from application.projectpermission.views import ProjectPermissionViewSets

router = routers.SimpleRouter(trailing_slash=False)
router.register('user/info', NormalUserViewSets, basename='user_info')
router.register('user/group', UserGroupViewSets, basename='user_group')
router.register('keyword/lib_keyword', LibKeywordViewSets, basename='lib_keyword')
router.register('keyword/user_keyword', UserKeywordViewSets, basename='user_keyword')
router.register('project', ProjectViewSets, basename='project')
router.register('suite_dir', SuiteDirViewSets, basename='suite_dir')
router.register('test_suite', TestSuiteViewSets, basename='test_suite')
router.register('test_case', TestCaseViewSets, basename='test_case')
router.register('case_entity', CaseEntityViewSets, basename='case_entity')
router.register('setup_teardown', SetupTeardownViewSets, basename='setup_teardown')
router.register('keyword_group', KeywordGroupViewSets, basename='keyword_group')
router.register('environment', EnvironmentViewSets, basename='environment')
router.register('region', RegionViewSets, basename='region')
router.register('variable', VariableViewSets, basename='variable')
router.register('project_version', ProjectVersionViewSets, basename='project_version')
router.register('build/plan', BuildPlanViewSets, basename='build_plan')
router.register('build/record', BuildRecordViewSets, basename='build_record')
router.register('build/history', BuildHistoryViewSets, basename='build_history')
router.register('tag', TagViewSets, basename='tag')
router.register('case_priority', CasePriorityViewSets, basename='case_priority')
router.register('builder', BuilderViewSets, basename='builder')
router.register('file/virtual_file', VirtualFileViewSets, basename='virtual_file')
router.register('file/project_file', ProjectFileViewSets, basename='project_file')
router.register('notice', NoticeViewSets, basename='notice')
router.register('permission_project', ProjectPermissionViewSets, basename='permission_project')


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/admin/', include(admin_router.urls)),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path(r'api/user/login', NoAuthUserViewSets.as_view({'post': 'login'})),
    path(r'api/user/register', NoAuthUserViewSets.as_view({'post': 'register'})),
    path(r'api/user/reset', NoAuthUserViewSets.as_view({'post': 'reset'})),
    path(r'api/internal/download_file', InternalFileViewSets.as_view({'post': 'download_file'}))
]
