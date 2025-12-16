"""
Serializers for Payment management
"""
from rest_framework import serializers
from apps.finance.models import Payment
from apps.students.serializers import StudentSerializer
from decimal import Decimal


class PaymentListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing payments
    """
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    registration_number = serializers.CharField(source='student.registration_number', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'student_name',
            'registration_number',
            'amount',
            'payment_method',
            'transaction_id',
            'payment_date',
            'is_verified',
            'verified_by_name',
            'verification_date',
            'fee_statement',
            'graduation_fee_amount',
            'created_at'
        ]
        read_only_fields = ['id', 'graduation_fee_amount', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    """
    Full serializer for payment CRUD operations
    """
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    verified_by_name = serializers.CharField(source='verified_by.full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'student',
            'student_id',
            'amount',
            'payment_method',
            'transaction_id',
            'phone_number',
            'payment_date',
            'is_verified',
            'verified_by',
            'verified_by_name',
            'verification_date',
            'notes',
            'receipt',
            'fee_statement',
            'graduation_fee_amount',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'is_verified',
            'verified_by',
            'verification_date',
            'graduation_fee_amount',
            'created_at',
            'updated_at'
        ]
    
    def validate_student_id(self, value):
        """Validate student exists and doesn't have existing payment"""
        from apps.students.models import Student
        
        try:
            student = Student.objects.get(id=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student not found")
        
        # Check if student already has a payment record
        if Payment.objects.filter(student=student).exists():
            # Allow if updating existing record
            if self.instance and self.instance.student == student:
                return value
            raise serializers.ValidationError(
                "Payment record already exists for this student"
            )
        
        return value
    
    def validate_amount(self, value):
        """Validate amount is positive and matches graduation fee"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        
        # For graduation fee payments, ensure amount is exactly 10,000
        graduation_fee = Decimal('10000.00')
        if value != graduation_fee:
            raise serializers.ValidationError(
                f"Payment amount must be exactly KES {graduation_fee:,.2f} (graduation fee)"
            )
        
        return value
    
    def validate_phone_number(self, value):
        """Validate phone number format (Kenya format)"""
        if value:
            # Remove spaces and special characters
            cleaned = value.replace(' ', '').replace('-', '').replace('+', '')
            
            # Check if it's a valid Kenyan number
            if not cleaned.isdigit():
                raise serializers.ValidationError("Phone number must contain only digits")
            
            # Kenya numbers: 254... or 07... or 01...
            if not (cleaned.startswith('254') or cleaned.startswith('07') or cleaned.startswith('01')):
                raise serializers.ValidationError(
                    "Phone number must be a valid Kenyan number (254..., 07..., or 01...)"
                )
            
            # Normalize to 254 format
            if cleaned.startswith('0'):
                cleaned = '254' + cleaned[1:]
            
            return cleaned
        
        return value
    
    def validate(self, attrs):
        """Additional validation"""
        payment_method = attrs.get('payment_method', self.instance.payment_method if self.instance else None)
        phone_number = attrs.get('phone_number', self.instance.phone_number if self.instance else None)
        
        # M-PESA requires phone number
        if payment_method == 'mpesa' and not phone_number:
            raise serializers.ValidationError({
                'phone_number': 'Phone number is required for M-PESA payments'
            })
        
        return attrs


class PaymentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new payment record
    """
    student_id = serializers.IntegerField()
    
    class Meta:
        model = Payment
        fields = [
            'student_id',
            'amount',
            'payment_method',
            'phone_number',
            'transaction_id',
            'notes',
            'receipt'
        ]
    
    def validate_student_id(self, value):
        """Validate student exists and doesn't have existing payment"""
        from apps.students.models import Student
        
        try:
            student = Student.objects.get(id=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student not found")
        
        # Check if student already has a payment record
        if Payment.objects.filter(student=student).exists():
            raise serializers.ValidationError(
                "Payment record already exists for this student. Use update instead."
            )
        
        return value
    
    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value
    
    def validate_phone_number(self, value):
        """Validate and normalize phone number"""
        if value:
            # Remove spaces and special characters
            cleaned = value.replace(' ', '').replace('-', '').replace('+', '')
            
            # Check if it's a valid Kenyan number
            if not cleaned.isdigit():
                raise serializers.ValidationError("Phone number must contain only digits")
            
            # Normalize to 254 format
            if cleaned.startswith('0'):
                cleaned = '254' + cleaned[1:]
            elif not cleaned.startswith('254'):
                raise serializers.ValidationError(
                    "Phone number must be a valid Kenyan number (254... or 07...)"
                )
            
            return cleaned
        
        return value
    
    def validate(self, attrs):
        """Additional validation"""
        payment_method = attrs.get('payment_method')
        phone_number = attrs.get('phone_number')
        
        # M-PESA requires phone number
        if payment_method == 'mpesa' and not phone_number:
            raise serializers.ValidationError({
                'phone_number': 'Phone number is required for M-PESA payments'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create payment record"""
        from apps.students.models import Student
        
        student_id = validated_data.pop('student_id')
        student = Student.objects.get(id=student_id)
        
        payment = Payment.objects.create(
            student=student,
            **validated_data
        )
        
        return payment


class MPESASTKPushSerializer(serializers.Serializer):
    """
    Serializer for M-PESA STK Push request
    """
    phone_number = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    account_reference = serializers.CharField(required=False, default='Clearance Fee')
    transaction_desc = serializers.CharField(required=False, default='Graduation Clearance Payment')
    
    def validate_phone_number(self, value):
        """Validate and normalize phone number"""
        # Remove spaces and special characters
        cleaned = value.replace(' ', '').replace('-', '').replace('+', '')
        
        # Check if it's a valid Kenyan number
        if not cleaned.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits")
        
        # Normalize to 254 format
        if cleaned.startswith('0'):
            cleaned = '254' + cleaned[1:]
        elif not cleaned.startswith('254'):
            raise serializers.ValidationError(
                "Phone number must be a valid Kenyan number (254... or 07...)"
            )
        
        # Validate length (254 + 9 digits = 12)
        if len(cleaned) != 12:
            raise serializers.ValidationError(
                "Phone number must be 12 digits in format 254XXXXXXXXX"
            )
        
        return cleaned
    
    def validate_amount(self, value):
        """Validate amount is positive and reasonable"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        
        if value > 150000:  # M-PESA limit
            raise serializers.ValidationError("Amount exceeds M-PESA transaction limit (150,000 KES)")
        
        return value


class PaymentVerificationSerializer(serializers.Serializer):
    """
    Serializer for payment verification
    """
    verify = serializers.BooleanField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        """Validate verification data"""
        payment = self.context.get('payment')
        
        if not payment:
            raise serializers.ValidationError("Payment not found")
        
        if payment.is_verified:
            raise serializers.ValidationError(
                "Payment is already verified"
            )
        
        return attrs


class MPESACallbackSerializer(serializers.Serializer):
    """
    Serializer for M-PESA callback data
    """
    MerchantRequestID = serializers.CharField()
    CheckoutRequestID = serializers.CharField()
    ResultCode = serializers.IntegerField()
    ResultDesc = serializers.CharField()
    Amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    MpesaReceiptNumber = serializers.CharField(required=False)
    TransactionDate = serializers.CharField(required=False)
    PhoneNumber = serializers.CharField(required=False)


class PaymentStatisticsSerializer(serializers.Serializer):
    """
    Serializer for payment statistics
    """
    total_payments = serializers.IntegerField()
    verified_payments = serializers.IntegerField()
    unverified_payments = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    verified_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    payment_methods = serializers.DictField()
    verification_rate = serializers.FloatField()
