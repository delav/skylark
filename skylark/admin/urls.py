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
from rest_framework import routers
from application.libkeyword.views import AdminKeywordViewSets
from application.user.views import AdminUserViewSets
from application.usergroup.views import AdminUserGroupViewSets
from application.project.views import AdminProjectViewSets
from application.casepriority.views import AdminCasePriorityViewSets
from application.department.views import AdminDepartmentViewSets
from application.systemext.views import AdminSystemExtViewSets

admin_router = routers.SimpleRouter(trailing_slash=False)
admin_router.register('keyword', AdminKeywordViewSets, basename='admin_keyword')
admin_router.register('user', AdminUserViewSets, basename='admin_user')
admin_router.register('user_group', AdminUserGroupViewSets, basename='admin_user_group')
admin_router.register('project', AdminProjectViewSets, basename='admin_project')
admin_router.register('priority', AdminCasePriorityViewSets, basename='admin_priority')
admin_router.register('department', AdminDepartmentViewSets, basename='admin_department')
admin_router.register('system', AdminSystemExtViewSets, basename='admin_system')
