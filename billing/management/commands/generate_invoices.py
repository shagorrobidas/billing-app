from django.core.management.base import BaseCommand
from billing.models import Customer, Invoice
from datetime import date


class Command(BaseCommand):
    help = 'Generate a set of invoices for all customers without an invoice for a specific month and year'

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            type=int,
            help='The year to generate invoices for. Defaults to the current year.',
            default=date.today().year,
        )
        parser.add_argument(
            '--month',
            type=int,
            help='The month to generate invoices for. Defaults to the current month.',
            default=date.today().month,
        )

    def handle(self, *args, **kwargs):
        year = kwargs['year']
        month = kwargs['month']

        customers = Customer.objects.all()
        for customer in customers:
            # Check if the customer already has an invoice for the specified month and year
            if not Invoice.objects.filter(customer=customer, date_created__month=month, date_created__year=year).exists():
                invoice_number = f"INVO-{year}-{month}-{customer.id}"
                invoice = Invoice.objects.create(
                    customer=customer,
                    invoice_number=invoice_number,
                    due_date=date.today(),
                    total_amount=10000.00,  # This can be dynamic based on your logic
                )
                self.stdout.write(f"Generated invoice: {invoice_number} for {customer.name}")
            else:
                self.stdout.write(f"Customer {customer.name} already has an invoice for {month}/{year}")
                
# class Command(BaseCommand):
#     help = 'Generate invoices for all customers'

#     def handle(self, *args, **options):
#         customers = Customer.objects.all()
#         for customer in customers:
#             invoice = Invoice(
#                 customer=customer,
#                 invoice_number=f'{customer.name[:3].upper()}-{date.today().strftime("%Y%m%d")}',
#                 due_date=date.today(),
#                 total_amount=1000,
#             )
#             invoice.save()
#             self.stdout.write(self.style.SUCCESS(f'Invoice {invoice.invoice_number} created for {customer.name}'))