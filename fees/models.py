from django.db import models
from django.core.validators import MinValueValidator
from students.models import Student, Class # Import your existing models

class FeeCategory(models.Model):
    """Types of fees: Tuition, Admission, Transport, Exam, etc."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Fee Categories"

class FeeStructure(models.Model):
    """Defines how much each Class pays for a specific FeeCategory."""
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_recurring = models.BooleanField(default=True, help_text="Is this a monthly fee?")

    def __str__(self):
        return f"{self.student_class.name} - {self.category.name} ({self.amount})"

    class Meta:
        unique_together = ('student_class', 'category')

class Invoice(models.Model):
    """The bill generated for a student for a specific period."""
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices')
    month = models.IntegerField(choices=[(i, i) for i in range(1, 13)]) # 1 for Jan, 12 for Dec
    year = models.IntegerField(default=2026)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def balance(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f"Inv #{self.id} - {self.student.name} ({self.month}/{self.year})"

class Transaction(models.Model):
    """Individual payment records (A student might pay one invoice in two parts)."""
    PAYMENT_MODES = [
        ('cash', 'Cash'),
        ('online', 'Online/UPI'),
        ('cheque', 'Cheque'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='transactions')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODES, default='cash')
    reference_number = models.CharField(max_length=100, blank=True, null=True, help_text="Transaction ID or Cheque No.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Auto-update the parent Invoice status whenever a payment is made
        inv = self.invoice
        total_received = inv.transactions.aggregate(models.Sum('amount_paid'))['amount_paid__sum'] or 0
        inv.paid_amount = total_received
        
        if inv.paid_amount >= inv.total_amount:
            inv.status = 'paid'
        elif inv.paid_amount > 0:
            inv.status = 'partial'
        else:
            inv.status = 'unpaid'
        inv.save()

    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.invoice.student.name}"