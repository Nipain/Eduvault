from django.urls import path
from . import views 
urlpatterns = [
    path('dashboard/', views.fee_dashboard, name='fee_dashboard'),
    path('generate/', views.generate_monthly_invoices, name='generate_fees'),
    # path('pay/<int:invoice_id>/', views.collect_payment, name='collect_payment'),
    path('collect-payment/<int:student_id>/', views.collect_payment, name='collect_payment'),
    path('history/<int:student_id>/', views.student_fee_history, name='student_fee_history'),
]

