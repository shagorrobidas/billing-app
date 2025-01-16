from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('invoice/<int:invoice_id>/create_payment/', views.create_payment, name='create_payment'),
]
