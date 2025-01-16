from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True)
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer.name}"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (f"Payment for {self.invoice.invoice_number} on {self.payment_date}")

