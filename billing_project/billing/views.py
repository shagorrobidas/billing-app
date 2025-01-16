from django.shortcuts import render, get_object_or_404
from .models import Invoice, Payment
from .forms import InvoiceForm, PaymentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


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
