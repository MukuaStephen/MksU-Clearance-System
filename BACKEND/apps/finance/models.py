import uuid
from django.db import models
from apps.students.models import Student
from apps.users.models import User


class FinanceRecord(models.Model):
    """Finance and payment information for student"""
    
    FEE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('verified', 'Verified'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='finance_record',
        help_text="Student finance information"
    )
    tuition_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Outstanding tuition balance in KES"
    )
    graduation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=5500.00,
        help_text="Graduation fee amount in KES"
    )
    graduation_fee_status = models.CharField(
        max_length=20,
        choices=FEE_STATUS_CHOICES,
        default='pending',
        help_text="Graduation fee payment status"
    )
    mpesa_code = models.CharField(
        max_length=50,
        blank=True,
        help_text="M-PESA confirmation code for graduation fee"
    )
    mpesa_payment_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date of M-PESA payment"
    )
    last_verified_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last date when fees were verified"
    )
    verified_by = models.CharField(
        max_length=255,
        blank=True,
        help_text="Finance staff who verified the payment"
    )
    notes = models.TextField(
        blank=True,
        help_text="Finance notes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'finance_records'
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['graduation_fee_status']),
        ]
    
    def __str__(self):
        return f"Finance - {self.student.user.full_name}"
    
    def verify_payment(self, verified_by):
        """Mark payment as verified"""
        from django.utils import timezone
        self.graduation_fee_status = 'verified'
        self.verified_by = verified_by
        self.last_verified_date = timezone.now()
        self.save()


class Payment(models.Model):
    """Payment record for clearance fees"""

    PAYMENT_METHODS = [
        ('mpesa', 'M-PESA'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='payment',
        help_text='Student payment record',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Payment amount',
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='mpesa',
        help_text='Payment method used',
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        help_text='Transaction or receipt number',
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        help_text='Payer phone number (for M-PESA)',
    )
    payment_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When payment was made',
    )
    is_verified = models.BooleanField(
        default=False,
        help_text='Whether payment has been verified',
    )
    verified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='verified_payments',
        help_text='User who verified the payment',
    )
    verification_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When payment was verified',
    )
    notes = models.TextField(
        blank=True,
        help_text='Payment notes',
    )
    receipt = models.FileField(
        upload_to='receipts/',
        null=True,
        blank=True,
        help_text='Uploaded receipt',
    )
    fee_statement = models.FileField(
        upload_to='fee_statements/',
        null=True,
        blank=True,
        help_text='Uploaded fee statement document',
    )
    graduation_fee_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=10000.00,
        help_text='Required graduation fee amount (KES 10,000)',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['payment_method']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Payment {self.transaction_id or self.id} - {self.student.user.full_name}"
    
    def clean(self):
        """Validate graduation fee amount"""
        from django.core.exceptions import ValidationError
        if self.graduation_fee_amount != 10000.00:
            raise ValidationError({
                'graduation_fee_amount': 'Graduation fee must be exactly KES 10,000'
            })
    
    def save(self, *args, **kwargs):
        """Ensure graduation fee is always KES 10,000"""
        self.graduation_fee_amount = 10000.00
        self.full_clean()
        super().save(*args, **kwargs)
