from django.shortcuts import render, get_object_or_404,redirect
from .models import Invoice, Payment
from .forms import (
    InvoiceForm,
    PaymentForm,
    UserRegistrationForm,
    UserLoginForm
)
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages



def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('invoice_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('invoice_list')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')




def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoice_list.html', {'invoices': invoices})


def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    payments = Payment.objects.filter(invoice=invoice)
    return render(request, 'invoice_detail.html', {'invoice': invoice, 'payments': payments})


def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('invoice_list'))
    else:
        form = InvoiceForm()
    return render(request, 'create_invoice.html', {'form': form})


def create_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()
            return HttpResponseRedirect(reverse('invoice_detail', args=[invoice_id]))
    else:
        form = PaymentForm()
    return render(request, 'create_payment.html', {'form': form, 'invoice': invoice})


