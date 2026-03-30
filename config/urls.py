"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from accounts import views as auth_views
from tenants.admin import tenant_admin_site

urlpatterns = [
    path("admin/", admin.site.urls),
    path('tenant-admin/', tenant_admin_site.urls),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view),

    path("dashboard/", auth_views.dashboard),

    path("admin-dashboard/", auth_views.admin_dashboard),
    path("teacher-dashboard/", auth_views.teacher_dashboard),
    path("parent-dashboard/", auth_views.parent_dashboard),
    path("accountant-dashboard/", auth_views.accountant_dashboard),
    # Student app 
    path("students/", include("students.urls")),
    path("fees/", include("fees.urls")),
]