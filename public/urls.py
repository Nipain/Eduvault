from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home),
    path('pricing/', views.pricing),
    path('signup/', views.signup),
    path('login-redirect/', views.login_redirect),
]