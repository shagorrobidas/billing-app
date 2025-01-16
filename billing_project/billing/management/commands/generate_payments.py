from django.core.management.base import BaseCommand
from billing.models import Invoice, Payment
from datetime import date
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Generate payments for unpaid invoices'

    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            type=float,
            help='The amount of payment to generate. Defaults to a random value.',
            default=None,
        )
        parser.add_argument(
            '--invoice_id',
            type=int,
            help='Generate payment for a specific invoice ID.',
            default=None,
        )
    
    def handle(self, *args, **kwargs):
        # Get the amount to pay (either specified or random)
        amount = kwargs['amount']
        if amount is None:
            amount = random.uniform(50.00, 200.00)  # Random payment amount between 50 and 200
        
        # Convert amount to decimal.Decimal for accurate financial calculations
        amount = Decimal(amount)
        
        # Get the invoice ID (if provided)
        invoice_id = kwargs['invoice_id']
        
        # If invoice_id is provided, find that specific invoice, else process all pending invoices
        if invoice_id:
            invoices = Invoice.objects.filter(id=invoice_id, status='PENDING')
            if not invoices.exists():
                self.stdout.write(f"No pending invoice found with ID {invoice_id}.")
                return
        else:
            invoices = Invoice.objects.filter(status='PENDING')
        
        for invoice in invoices:
            # Convert the invoice's total_amount to decimal.Decimal for consistent comparison
            total_amount = Decimal(invoice.total_amount)

            # If the invoice is pending, create a payment for it
            if total_amount > 0 and (total_amount - amount) >= 0:
                payment = Payment.objects.create(
                    invoice=invoice,
                    payment_date=date.today(),
                    amount=amount,
                )
                
                # Update invoice status if it is fully paid
                if total_amount - amount <= 0:
                    invoice.status = 'PAID'
                    invoice.save()

                self.stdout.write(f"Generated payment of {amount:.2f} for Invoice {invoice.invoice_number}.")
            else:
                self.stdout.write(f"Payment of {amount:.2f} exceeds the amount due for Invoice {invoice.invoice_number}.")
