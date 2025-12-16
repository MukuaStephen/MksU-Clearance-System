"""
Views for Payment management with M-PESA integration
"""
from rest_framework import viewsets, filters, status, serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.conf import settings
import requests
import base64
import json
from datetime import datetime

from apps.finance.models import Payment
from apps.finance.serializers import (
    PaymentSerializer,
    PaymentListSerializer,
    PaymentCreateSerializer,
    MPESASTKPushSerializer,
    PaymentVerificationSerializer,
    MPESACallbackSerializer,
    PaymentStatisticsSerializer
)
from apps.users.permissions import IsAdmin, IsStudentOwnerOrAdmin
from apps.students.models import Student
from apps.notifications.utils import (
    notify_payment_verified,
    notify_payment_failed,
)
from apps.audit_logs.mixins import AuditViewSetMixin


class PaymentViewSet(AuditViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for Payment CRUD operations
    
    Permissions:
    - List/Retrieve: Students see own payment, Admins see all
    - Create: Students (for themselves), Admins (for any student)
    - Update: Admins only
    - Delete: Admins only
    - verify: Admins only
    """
    queryset = Payment.objects.select_related('student__user', 'verified_by').all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'payment_method',
        'is_verified',
        'student__faculty',
        'student__program',
        'student__graduation_year'
    ]
    search_fields = [
        'transaction_id',
        'student__registration_number',
        'student__user__full_name',
        'student__user__admission_number',
        'phone_number'
    ]
    ordering_fields = ['created_at', 'payment_date', 'amount', 'verification_date']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'list':
            return PaymentListSerializer
        elif self.action == 'create':
            return PaymentCreateSerializer
        elif self.action == 'mpesa_stk_push':
            return MPESASTKPushSerializer
        elif self.action == 'verify':
            return PaymentVerificationSerializer
        return PaymentSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user role
        Students see only their own payment
        """
        user = self.request.user
        
        if user.role == 'admin':
            # Admins see all payments
            return Payment.objects.select_related('student__user', 'verified_by').all()
        elif user.role == 'student':
            # Students see only their own payment
            try:
                student = Student.objects.get(user=user)
                return Payment.objects.filter(student=student).select_related('student__user', 'verified_by')
            except Student.DoesNotExist:
                return Payment.objects.none()
        elif user.role == 'department_staff':
            # Department staff can see all payments (for clearance processing)
            return Payment.objects.select_related('student__user', 'verified_by').all()
        
        return Payment.objects.none()
    
    def get_permissions(self):
        """Set different permissions based on action"""
        if self.action in ['update', 'partial_update', 'destroy', 'verify']:
            # Only admins can update, delete, or verify
            return [IsAuthenticated(), IsAdmin()]
        elif self.action == 'mpesa_callback':
            # Callback doesn't require authentication (comes from M-PESA)
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """
        Create payment record
        Students can only create for themselves
        """
        user = self.request.user
        
        if user.role == 'student':
            # Get student record
            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                raise serializers.ValidationError({
                    'error': 'Student record not found'
                })
            
            # Ensure student_id matches authenticated user
            student_id = serializer.validated_data.get('student_id')
            if student_id != student.id:
                raise serializers.ValidationError({
                    'error': 'You can only create payment records for yourself'
                })
        
        serializer.save()
    
    @action(detail=False, methods=['post'])
    def mpesa_stk_push(self, request):
        """
        Initiate M-PESA STK Push payment
        POST /api/finance/mpesa_stk_push/
        Body: {
            "phone_number": "254712345678",
            "amount": 1000
        }
        """
        user = request.user
        
        # Only students can initiate payment for themselves
        if user.role != 'student':
            return Response(
                {'error': 'Only students can initiate M-PESA payments'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get student record
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student record not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if student already has a verified payment
        existing_payment = Payment.objects.filter(student=student, is_verified=True).first()
        if existing_payment:
            return Response(
                {
                    'error': 'You have already paid clearance fees',
                    'payment': PaymentSerializer(existing_payment).data
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        amount = serializer.validated_data['amount']
        account_reference = serializer.validated_data.get('account_reference', 'Clearance Fee')
        transaction_desc = serializer.validated_data.get('transaction_desc', 'Graduation Clearance')
        
        # Initiate M-PESA STK Push
        result = self._initiate_mpesa_stk_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=account_reference,
            transaction_desc=transaction_desc,
            student=student
        )
        
        if result.get('success'):
            # Create or update payment record
            payment, created = Payment.objects.get_or_create(
                student=student,
                defaults={
                    'amount': amount,
                    'payment_method': 'mpesa',
                    'phone_number': phone_number,
                    'notes': 'M-PESA STK Push initiated'
                }
            )
            
            if not created:
                payment.amount = amount
                payment.phone_number = phone_number
                payment.payment_method = 'mpesa'
                payment.notes = f'M-PESA STK Push initiated at {timezone.now()}'
                payment.save()
            
            return Response({
                'message': 'M-PESA STK Push sent successfully. Please enter your PIN on your phone.',
                'checkout_request_id': result.get('checkout_request_id'),
                'merchant_request_id': result.get('merchant_request_id'),
                'payment_id': payment.id
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Failed to initiate M-PESA payment',
                'details': result.get('error')
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def _initiate_mpesa_stk_push(self, phone_number, amount, account_reference, transaction_desc, student):
        """
        Internal method to initiate M-PESA STK Push
        """
        # M-PESA Credentials (should be in environment variables)
        business_short_code = getattr(settings, 'MPESA_SHORTCODE', '174379')
        passkey = getattr(settings, 'MPESA_PASSKEY', 'your_passkey_here')
        consumer_key = getattr(settings, 'MPESA_CONSUMER_KEY', '')
        consumer_secret = getattr(settings, 'MPESA_CONSUMER_SECRET', '')
        api_url = getattr(settings, 'MPESA_API_URL', 'https://sandbox.safaricom.co.ke')
        
        # Check if credentials are configured
        if not consumer_key or not consumer_secret:
            return {
                'success': False,
                'error': 'M-PESA credentials not configured. Please contact administrator.'
            }
        
        try:
            # Get access token
            auth_url = f'{api_url}/oauth/v1/generate?grant_type=client_credentials'
            auth_response = requests.get(
                auth_url,
                auth=(consumer_key, consumer_secret)
            )
            
            if auth_response.status_code != 200:
                return {
                    'success': False,
                    'error': 'Failed to get M-PESA access token'
                }
            
            access_token = auth_response.json().get('access_token')
            
            # Prepare STK Push request
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode(
                f'{business_short_code}{passkey}{timestamp}'.encode()
            ).decode('utf-8')
            
            callback_url = getattr(
                settings,
                'MPESA_CALLBACK_URL',
                'https://yourdomain.com/api/finance/mpesa_callback/'
            )
            
            stk_push_url = f'{api_url}/mpesa/stkpush/v1/processrequest'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'BusinessShortCode': business_short_code,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': int(amount),
                'PartyA': phone_number,
                'PartyB': business_short_code,
                'PhoneNumber': phone_number,
                'CallBackURL': callback_url,
                'AccountReference': f'{student.registration_number}',
                'TransactionDesc': transaction_desc
            }
            
            response = requests.post(stk_push_url, json=payload, headers=headers)
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get('ResponseCode') == '0':
                return {
                    'success': True,
                    'checkout_request_id': response_data.get('CheckoutRequestID'),
                    'merchant_request_id': response_data.get('MerchantRequestID')
                }
            else:
                return {
                    'success': False,
                    'error': response_data.get('errorMessage', 'Unknown error')
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify a payment (admin only)
        POST /api/finance/{id}/verify/
        Body: {"verify": true, "notes": "..."}
        """
        payment = self.get_object()
        
        # Validate request
        serializer = self.get_serializer(
            data=request.data,
            context={'payment': payment}
        )
        serializer.is_valid(raise_exception=True)
        
        verify = serializer.validated_data['verify']
        notes = serializer.validated_data.get('notes', '')
        
        if verify:
            payment.is_verified = True
            payment.verified_by = request.user
            payment.verification_date = timezone.now()
            if notes:
                payment.notes = f'{payment.notes}\nVerified: {notes}' if payment.notes else notes
            else:
                payment.notes = f'{payment.notes}\nVerified by {request.user.full_name}' if payment.notes else f'Verified by {request.user.full_name}'
            payment.save()
            
            # Notify student payment verified
            notify_payment_verified(payment)
            
            return Response({
                'message': 'Payment verified successfully',
                'payment': PaymentSerializer(payment).data
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Verification cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def my_payment(self, request):
        """
        Get current student's payment record
        GET /api/finance/my_payment/
        Students only
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student record not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            payment = Payment.objects.get(student=student)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        except Payment.DoesNotExist:
            return Response(
                {
                    'message': 'No payment record found',
                    'has_paid': False
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def unverified(self, request):
        """
        Get unverified payments (admin only)
        GET /api/finance/unverified/
        """
        if request.user.role != 'admin':
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        payments = Payment.objects.filter(
            is_verified=False
        ).select_related('student__user')
        
        serializer = PaymentListSerializer(payments, many=True)
        return Response({
            'count': payments.count(),
            'payments': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get payment statistics
        GET /api/finance/statistics/
        Admin only
        """
        if request.user.role != 'admin':
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Calculate statistics
        total_payments = Payment.objects.count()
        verified_payments = Payment.objects.filter(is_verified=True).count()
        unverified_payments = total_payments - verified_payments
        
        total_amount = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
        verified_amount = Payment.objects.filter(
            is_verified=True
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Payment methods breakdown
        payment_methods = {}
        for method, label in Payment.PAYMENT_METHODS:
            count = Payment.objects.filter(payment_method=method).count()
            payment_methods[label] = count
        
        verification_rate = (verified_payments / total_payments * 100) if total_payments > 0 else 0
        
        return Response({
            'total_payments': total_payments,
            'verified_payments': verified_payments,
            'unverified_payments': unverified_payments,
            'total_amount': float(total_amount),
            'verified_amount': float(verified_amount),
            'payment_methods': payment_methods,
            'verification_rate': round(verification_rate, 2)
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def mpesa_callback(request):
    """
    M-PESA callback endpoint
    POST /api/finance/mpesa_callback/
    Receives payment confirmation from M-PESA
    """
    try:
        data = request.data
        
        # Extract callback data
        body = data.get('Body', {}).get('stkCallback', {})
        
        merchant_request_id = body.get('MerchantRequestID')
        checkout_request_id = body.get('CheckoutRequestID')
        result_code = body.get('ResultCode')
        result_desc = body.get('ResultDesc')
        
        # Log callback for debugging
        print(f'M-PESA Callback: {json.dumps(data, indent=2)}')
        
        if result_code == 0:
            # Payment successful
            callback_metadata = body.get('CallbackMetadata', {}).get('Item', [])
            
            # Extract transaction details
            transaction_details = {}
            for item in callback_metadata:
                name = item.get('Name')
                value = item.get('Value')
                transaction_details[name] = value
            
            amount = transaction_details.get('Amount')
            mpesa_receipt = transaction_details.get('MpesaReceiptNumber')
            transaction_date = transaction_details.get('TransactionDate')
            phone_number = transaction_details.get('PhoneNumber')
            
            # Find payment record by phone number
            if phone_number:
                # Normalize phone number
                phone_str = str(phone_number)
                
                payment = Payment.objects.filter(
                    phone_number__contains=phone_str[-9:],  # Match last 9 digits
                    payment_method='mpesa',
                    is_verified=False
                ).first()
                
                if payment:
                    # Update payment record
                    payment.transaction_id = mpesa_receipt
                    payment.payment_date = timezone.now()
                    payment.is_verified = True
                    payment.notes = f'{payment.notes}\nM-PESA Payment successful. Receipt: {mpesa_receipt}'
                    payment.save()
                    
                    # Notify student payment verified
                    notify_payment_verified(payment)
        
        else:
            # Payment failed
            print(f'M-PESA Payment Failed: {result_desc}')
            # Try to notify failure if a pending payment exists for phone
            try:
                phone_items = body.get('CallbackMetadata', {}).get('Item', [])
                phone_vals = [i.get('Value') for i in phone_items if i.get('Name') == 'PhoneNumber']
                if phone_vals:
                    phone = str(phone_vals[0])
                    payment = Payment.objects.filter(
                        phone_number__contains=phone[-9:],
                        payment_method='mpesa',
                        is_verified=False
                    ).first()
                    if payment:
                        notify_payment_failed(payment)
            except Exception:
                pass
        
        return Response({
            'ResultCode': 0,
            'ResultDesc': 'Success'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f'M-PESA Callback Error: {str(e)}')
        return Response({
            'ResultCode': 1,
            'ResultDesc': str(e)
        }, status=status.HTTP_200_OK)
