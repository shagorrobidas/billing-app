from django.core.management.base import BaseCommand
from billing.models import Customer  # Import the Customer model
from faker import Faker

class Command(BaseCommand):
    help = 'Generate 20 random customers for testing purposes'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create 20 random customers
        for _ in range(20):
            customer = Customer.objects.create(
                name=fake.name(),
                email=fake.email(),
                # phone_number=fake.phone_number(),
                address=fake.address(),
                
                # Add any other fields here based on your Customer model
            )
            self.stdout.write(f"Generated customer: {customer.name} ({customer.email})")
