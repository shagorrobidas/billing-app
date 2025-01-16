from django.core.management.base import BaseCommand
from billing.models import Invoice
from datetime import date

class Command(BaseCommand):
    help = 'Send payment reminders for overdue invoices'

    def handle(self, *args, **kwargs):
        today = date.today()
        overdue_invoices = Invoice.objects.filter(status='PENDING', due_date__lt=today)

        for invoice in overdue_invoices:
            # Logic for sending reminders, e.g., sending an email
            # Example: sending a reminder (in real-world case, integrate with an email system)
            self.stdout.write(f"Reminder sent for Invoice: {invoice.invoice_number} (Due: {invoice.due_date})")

        if not overdue_invoices.exists():
            self.stdout.write("No overdue invoices found.")
