from django import forms
from .models import Invoice, Payment

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'invoice_number', 'due_date', 'total_amount', 'status']
        widgets = {
            'due_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'YYYY-MM-DD',
                },
                format='%Y-%m-%d'
            ),
            'customer': forms.Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'customer':  # Skip customer, already has custom widget
                field.widget.attrs.update({'class': 'form-control'})


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_date', 'amount']
        widgets = {
            'payment_date': forms.DateInput(
                attrs={
                    'type': 'date',  # Use HTML5 date input
                    'class': 'form-control',
                    'placeholder': 'YYYY-MM-DD',
                },
                format='%Y-%m-%d'  # Specify the date format
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'payment_date':  # Skip payment_date, already has custom widget
                field.widget.attrs.update({'class': 'form-control'})
