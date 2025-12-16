"""
Analytics Views for Dashboard and Reporting
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Avg, Q, F
from django.utils import timezone
from datetime import timedelta

from apps.clearances.models import ClearanceRequest
from apps.approvals.models import ClearanceApproval
from apps.students.models import Student
from apps.finance.models import Payment, FinanceRecord
from apps.departments.models import Department
from apps.users.permissions import IsAdminOrDepartmentStaff


class ClearanceCompletionRateView(APIView):
    """
    Analytics for clearance completion rates
    GET /api/analytics/clearance-completion/
    """
    permission_classes = [IsAuthenticated, IsAdminOrDepartmentStaff]
    
    def get(self, request):
        # Query parameters for filtering
        graduation_year = request.query_params.get('graduation_year')
        school_id = request.query_params.get('school_id')
        admission_year = request.query_params.get('admission_year')
        
        # Base queryset
        clearances = ClearanceRequest.objects.all()
        
        # Apply filters
        if graduation_year:
            clearances = clearances.filter(student__graduation_year=graduation_year)
        if school_id:
            clearances = clearances.filter(student__school_id=school_id)
        if admission_year:
            clearances = clearances.filter(student__admission_year=admission_year)
        
        # Overall statistics
        total_clearances = clearances.count()
        completed = clearances.filter(status='completed').count()
        in_progress = clearances.filter(status='in_progress').count()
        rejected = clearances.filter(status='rejected').count()
        pending = clearances.filter(status='pending').count()
        
        completion_rate = (completed / total_clearances * 100) if total_clearances > 0 else 0
        
        # By graduation year
        by_graduation_year = clearances.values('student__graduation_year').annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            in_progress=Count('id', filter=Q(status='in_progress')),
            rejected=Count('id', filter=Q(status='rejected'))
        ).order_by('-student__graduation_year')
        
        # By school
        by_school = clearances.values(
            'student__school__name',
            'student__school__code'
        ).annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            in_progress=Count('id', filter=Q(status='in_progress')),
            rejected=Count('id', filter=Q(status='rejected'))
        ).order_by('-total')
        
        # Average completion time (for completed clearances)
        completed_clearances = clearances.filter(status='completed', completion_date__isnull=False)
        avg_completion_days = None
        if completed_clearances.exists():
            completion_times = []
            for clearance in completed_clearances:
                days = (clearance.completion_date - clearance.submission_date).days
                completion_times.append(days)
            avg_completion_days = sum(completion_times) / len(completion_times) if completion_times else 0
        
        return Response({
            'summary': {
                'total_clearances': total_clearances,
                'completed': completed,
                'in_progress': in_progress,
                'rejected': rejected,
                'pending': pending,
                'completion_rate': round(completion_rate, 2),
                'average_completion_days': round(avg_completion_days, 1) if avg_completion_days else None
            },
            'by_graduation_year': list(by_graduation_year),
            'by_school': list(by_school)
        })


class DepartmentBottlenecksView(APIView):
    """
    Analytics for department approval bottlenecks
    GET /api/analytics/department-bottlenecks/
    """
    permission_classes = [IsAuthenticated, IsAdminOrDepartmentStaff]
    
    def get(self, request):
        # Get all departments
        departments = Department.objects.filter(is_active=True)
        
        bottleneck_data = []
        
        for dept in departments:
            # Approvals for this department
            approvals = ClearanceApproval.objects.filter(department=dept)
            
            total_approvals = approvals.count()
            pending = approvals.filter(status='pending').count()
            approved = approvals.filter(status='approved').count()
            rejected = approvals.filter(status='rejected').count()
            
            # Average approval time (for approved/rejected)
            processed = approvals.filter(status__in=['approved', 'rejected'], approval_date__isnull=False)
            avg_processing_days = None
            if processed.exists():
                processing_times = []
                for approval in processed:
                    days = (approval.approval_date - approval.created_at).days
                    processing_times.append(days)
                avg_processing_days = sum(processing_times) / len(processing_times) if processing_times else 0
            
            # Pending for more than 7 days
            seven_days_ago = timezone.now() - timedelta(days=7)
            overdue_pending = approvals.filter(
                status='pending',
                created_at__lt=seven_days_ago
            ).count()
            
            approval_rate = (approved / total_approvals * 100) if total_approvals > 0 else 0
            rejection_rate = (rejected / total_approvals * 100) if total_approvals > 0 else 0
            
            bottleneck_data.append({
                'department_name': dept.name,
                'department_code': dept.code,
                'department_type': dept.department_type,
                'approval_order': dept.approval_order,
                'total_approvals': total_approvals,
                'pending': pending,
                'approved': approved,
                'rejected': rejected,
                'overdue_pending': overdue_pending,
                'approval_rate': round(approval_rate, 2),
                'rejection_rate': round(rejection_rate, 2),
                'average_processing_days': round(avg_processing_days, 1) if avg_processing_days else None
            })
        
        # Sort by overdue_pending descending (bottlenecks first)
        bottleneck_data.sort(key=lambda x: x['overdue_pending'], reverse=True)
        
        return Response({
            'departments': bottleneck_data,
            'total_departments': len(bottleneck_data)
        })


class FinancialSummaryView(APIView):
    """
    Analytics for financial summaries by cohort/school
    GET /api/analytics/financial-summary/
    """
    permission_classes = [IsAuthenticated, IsAdminOrDepartmentStaff]
    
    def get(self, request):
        # Query parameters
        graduation_year = request.query_params.get('graduation_year')
        school_id = request.query_params.get('school_id')
        admission_year = request.query_params.get('admission_year')
        
        # Base queryset for payments
        payments = Payment.objects.all()
        students = Student.objects.all()
        
        # Apply filters
        if graduation_year:
            payments = payments.filter(student__graduation_year=graduation_year)
            students = students.filter(graduation_year=graduation_year)
        if school_id:
            payments = payments.filter(student__school_id=school_id)
            students = students.filter(school_id=school_id)
        if admission_year:
            payments = payments.filter(student__admission_year=admission_year)
            students = students.filter(admission_year=admission_year)
        
        # Overall payment statistics
        total_payments = payments.count()
        verified_payments = payments.filter(is_verified=True).count()
        pending_payments = payments.filter(is_verified=False).count()
        
        total_amount_paid = payments.aggregate(total=Sum('amount'))['total'] or 0
        total_graduation_fees = payments.aggregate(total=Sum('graduation_fee_amount'))['total'] or 0
        
        # By graduation year
        by_graduation_year = payments.values('student__graduation_year').annotate(
            total_students=Count('student__id', distinct=True),
            total_paid=Sum('amount'),
            verified_count=Count('id', filter=Q(is_verified=True)),
            pending_count=Count('id', filter=Q(is_verified=False))
        ).order_by('-student__graduation_year')
        
        # By school
        by_school = payments.values(
            'student__school__name',
            'student__school__code'
        ).annotate(
            total_students=Count('student__id', distinct=True),
            total_paid=Sum('amount'),
            verified_count=Count('id', filter=Q(is_verified=True)),
            pending_count=Count('id', filter=Q(is_verified=False))
        ).order_by('-total_paid')
        
        # By admission year
        by_admission_year = payments.values('student__admission_year').annotate(
            total_students=Count('student__id', distinct=True),
            total_paid=Sum('amount'),
            verified_count=Count('id', filter=Q(is_verified=True)),
            pending_count=Count('id', filter=Q(is_verified=False))
        ).order_by('-student__admission_year')
        
        # Payment methods breakdown
        by_payment_method = payments.values('payment_method').annotate(
            count=Count('id'),
            total_amount=Sum('amount')
        ).order_by('-count')
        
        # Students without payments
        total_students = students.count()
        students_with_payments = payments.values('student').distinct().count()
        students_without_payments = total_students - students_with_payments
        
        return Response({
            'summary': {
                'total_payments': total_payments,
                'verified_payments': verified_payments,
                'pending_payments': pending_payments,
                'total_amount_paid': float(total_amount_paid),
                'total_graduation_fees': float(total_graduation_fees),
                'total_students': total_students,
                'students_with_payments': students_with_payments,
                'students_without_payments': students_without_payments,
                'payment_compliance_rate': round((students_with_payments / total_students * 100), 2) if total_students > 0 else 0
            },
            'by_graduation_year': list(by_graduation_year),
            'by_school': list(by_school),
            'by_admission_year': list(by_admission_year),
            'by_payment_method': list(by_payment_method)
        })


class OverallDashboardView(APIView):
    """
    Comprehensive dashboard with key metrics
    GET /api/analytics/dashboard/
    """
    permission_classes = [IsAuthenticated, IsAdminOrDepartmentStaff]
    
    def get(self, request):
        # Students
        total_students = Student.objects.count()
        eligible_students = Student.objects.filter(eligibility_status='eligible').count()
        
        # Clearances
        total_clearances = ClearanceRequest.objects.count()
        completed_clearances = ClearanceRequest.objects.filter(status='completed').count()
        pending_clearances = ClearanceRequest.objects.filter(status='pending').count()
        in_progress_clearances = ClearanceRequest.objects.filter(status='in_progress').count()
        
        # Approvals
        total_approvals = ClearanceApproval.objects.count()
        pending_approvals = ClearanceApproval.objects.filter(status='pending').count()
        
        # Finance
        total_payments = Payment.objects.count()
        verified_payments = Payment.objects.filter(is_verified=True).count()
        total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
        
        # Recent activity (last 7 days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_clearances = ClearanceRequest.objects.filter(created_at__gte=seven_days_ago).count()
        recent_payments = Payment.objects.filter(created_at__gte=seven_days_ago).count()
        
        # Gown issuance (if available)
        try:
            from apps.gown_issuance.models import GownIssuance
            total_gowns_issued = GownIssuance.objects.count()
            gowns_returned = GownIssuance.objects.filter(status='returned').count()
            gowns_overdue = GownIssuance.objects.filter(
                status='issued',
                expected_return_date__lt=timezone.now().date()
            ).count()
        except:
            total_gowns_issued = 0
            gowns_returned = 0
            gowns_overdue = 0
        
        return Response({
            'students': {
                'total': total_students,
                'eligible': eligible_students,
                'eligibility_rate': round((eligible_students / total_students * 100), 2) if total_students > 0 else 0
            },
            'clearances': {
                'total': total_clearances,
                'completed': completed_clearances,
                'in_progress': in_progress_clearances,
                'pending': pending_clearances,
                'completion_rate': round((completed_clearances / total_clearances * 100), 2) if total_clearances > 0 else 0
            },
            'approvals': {
                'total': total_approvals,
                'pending': pending_approvals,
                'processing_rate': round(((total_approvals - pending_approvals) / total_approvals * 100), 2) if total_approvals > 0 else 0
            },
            'finance': {
                'total_payments': total_payments,
                'verified_payments': verified_payments,
                'total_revenue': float(total_revenue),
                'verification_rate': round((verified_payments / total_payments * 100), 2) if total_payments > 0 else 0
            },
            'gown_issuance': {
                'total_issued': total_gowns_issued,
                'returned': gowns_returned,
                'overdue': gowns_overdue
            },
            'recent_activity': {
                'clearances_last_7_days': recent_clearances,
                'payments_last_7_days': recent_payments
            }
        })
