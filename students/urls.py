from django.urls import path
from . import views 
urlpatterns = [
    path("add/", views.add_student, name="add_student"),
    path("list/", views.student_list, name="student_list"),
    path('edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('promote/<int:pk>/', views.promote_student, name='promote_student'),
]