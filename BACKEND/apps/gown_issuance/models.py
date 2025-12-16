import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.students.models import Student
from apps.users.models import User


class GownIssuance(models.Model):
    """Track graduation gown issuance, returns, and deposits"""
    
    STATUS_CHOICES = [
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
    ]
    
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='gown_issuance',
        help_text="Student issued the gown"
    )
    gown_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique gown identifier/tag number"
    )
    gown_size = models.CharField(
        max_length=5,
        choices=SIZE_CHOICES,
        help_text="Gown size"
    )
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=2000.00,
        help_text="Deposit amount in KES (refundable on return)"
    )
    deposit_paid = models.BooleanField(
        default=False,
        help_text="Whether deposit has been paid"
    )
    deposit_receipt = models.CharField(
        max_length=100,
        blank=True,
        help_text="Receipt number for deposit payment"
    )
    issued_date = models.DateTimeField(
        default=timezone.now,
        help_text="Date gown was issued"
    )
    issued_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='gowns_issued',
        help_text="Staff who issued the gown"
    )
    expected_return_date = models.DateField(
        help_text="Expected date for gown return"
    )
    actual_return_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Actual date gown was returned"
    )
    returned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='gowns_received',
        help_text="Staff who received the returned gown"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='issued',
        help_text="Current status of gown"
    )
    condition_notes = models.TextField(
        blank=True,
        help_text="Notes on gown condition (damage, stains, etc.)"
    )
    deposit_refunded = models.BooleanField(
        default=False,
        help_text="Whether deposit has been refunded"
    )
    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount refunded (may be partial if damaged)"
    )
    refund_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date deposit was refunded"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gown_issuances'
        ordering = ['-issued_date']
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['gown_number']),
            models.Index(fields=['status']),
            models.Index(fields=['issued_date']),
            models.Index(fields=['expected_return_date']),
        ]
    
    def __str__(self):
        return f"Gown {self.gown_number} - {self.student.user.full_name} ({self.status})"
    
    def clean(self):
        """Validate gown issuance data"""
        if self.status == 'returned' and not self.actual_return_date:
            raise ValidationError({
                'actual_return_date': 'Return date required when status is returned'
            })
        
        if self.deposit_refunded and not self.refund_amount:
            raise ValidationError({
                'refund_amount': 'Refund amount required when deposit is refunded'
            })
    
    def mark_returned(self, returned_to, condition_notes=''):
        """Mark gown as returned"""
        self.status = 'returned'
        self.actual_return_date = timezone.now()
        self.returned_to = returned_to
        self.condition_notes = condition_notes
        self.save()
    
    def process_refund(self, refund_amount):
        """Process deposit refund"""
        if refund_amount > self.deposit_amount:
            raise ValidationError("Refund amount cannot exceed deposit amount")
        
        self.deposit_refunded = True
        self.refund_amount = refund_amount
        self.refund_date = timezone.now()
        self.save()
    
    @property
    def is_overdue(self):
        """Check if gown return is overdue"""
        if self.status == 'issued':
            return timezone.now().date() > self.expected_return_date
        return False
    
    @property
    def days_overdue(self):
        """Calculate days overdue"""
        if self.is_overdue:
            return (timezone.now().date() - self.expected_return_date).days
        return 0
