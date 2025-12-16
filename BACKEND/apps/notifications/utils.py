"""
Notification helper functions
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

from apps.notifications.models import Notification


def create_notification(
    recipient,
    notification_type,
    title,
    message,
    clearance=None,
    approval=None,
    payment=None,
    send_email=True
):
    """
    Create a notification and optionally send email
    
    Args:
        recipient: User object who will receive the notification
        notification_type: One of the NOTIFICATION_TYPES choices
        title: Notification title
        message: Notification message body
        clearance: Optional related ClearanceRequest object
        approval: Optional related ClearanceApproval object
        payment: Optional related Payment object
        send_email: Whether to send email notification (default True)
    
    Returns:
        Notification object
    """
    # Create notification
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        clearance=clearance,
        approval=approval,
        payment=payment
    )
    
    # Send email if requested
    if send_email:
        email_sent = send_email_notification(notification)
        if email_sent:
            notification.mark_email_sent()
    
    return notification


def send_email_notification(notification):
    """
    Send email notification using template
    
    Args:
        notification: Notification object
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        recipient_email = notification.recipient.email
        
        # Skip if no email
        if not recipient_email:
            return False
        
        # Determine template based on notification type
        template_mapping = {
            'clearance_submitted': 'notifications/emails/clearance_submitted.html',
            'clearance_approved': 'notifications/emails/clearance_approved.html',
            'clearance_rejected': 'notifications/emails/clearance_rejected.html',
            'payment_received': 'notifications/emails/payment_received.html',
            'payment_verified': 'notifications/emails/payment_verified.html',
            'approval_pending': 'notifications/emails/approval_pending.html',
        }
        
        template_name = template_mapping.get(
            notification.notification_type,
            'notifications/emails/generic.html'
        )
        
        # Render HTML email
        context = {
            'notification': notification,
            'recipient': notification.recipient,
            'site_name': 'MksU Clearance System',
            'site_url': settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:5173'
        }
        
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=notification.title,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False
        )
        
        return True
        
    except Exception as e:
        # Log the error (you can add proper logging here)
        print(f"Error sending email notification: {str(e)}")
        return False


def notify_clearance_submitted(clearance_request):
    """
    Notify student and admin when clearance is submitted
    
    Args:
        clearance_request: ClearanceRequest object
    """
    # Notify student
    create_notification(
        recipient=clearance_request.student.user,
        notification_type='clearance_submitted',
        title='Clearance Request Submitted',
        message=f'Your clearance request for {clearance_request.academic_year} {clearance_request.semester} has been submitted successfully. It is now pending approval.',
        clearance=clearance_request,
        send_email=True
    )
    
    # Notify admins
    from apps.users.models import User
    admins = User.objects.filter(role='admin', is_active=True)
    
    for admin in admins:
        create_notification(
            recipient=admin,
            notification_type='clearance_submitted',
            title='New Clearance Request',
            message=f'Student {clearance_request.student.user.get_full_name()} ({clearance_request.student.registration_number}) has submitted a clearance request.',
            clearance=clearance_request,
            send_email=False  # Don't spam admins with emails
        )


def notify_clearance_approved(clearance_request):
    """
    Notify student when clearance is fully approved
    
    Args:
        clearance_request: ClearanceRequest object
    """
    create_notification(
        recipient=clearance_request.student.user,
        notification_type='clearance_approved',
        title='Clearance Request Approved',
        message=f'Congratulations! Your clearance request for {clearance_request.academic_year} {clearance_request.semester} has been fully approved.',
        clearance=clearance_request,
        send_email=True
    )


def notify_clearance_rejected(clearance_request):
    """
    Notify student when clearance is rejected
    
    Args:
        clearance_request: ClearanceRequest object
    """
    create_notification(
        recipient=clearance_request.student.user,
        notification_type='clearance_rejected',
        title='Clearance Request Rejected',
        message=f'Your clearance request for {clearance_request.academic_year} {clearance_request.semester} has been rejected. Please check the approval details for more information.',
        clearance=clearance_request,
        send_email=True
    )


def notify_approval_action(approval):
    """
    Notify student about approval action (approved/rejected)
    
    Args:
        approval: ClearanceApproval object
    """
    action_text = 'approved' if approval.status == 'approved' else 'rejected'
    
    create_notification(
        recipient=approval.clearance_request.student.user,
        notification_type='approval_pending',  # Generic approval notification
        title=f'Department Approval: {action_text.title()}',
        message=f'The {approval.department.name} has {action_text} your clearance request.',
        approval=approval,
        clearance=approval.clearance_request,
        send_email=True
    )


def notify_approval_pending(approval):
    """
    Notify department staff about pending approval
    
    Args:
        approval: ClearanceApproval object
    """
    # Get department staff
    from apps.users.models import User
    staff = User.objects.filter(
        role='department_staff',
        department=approval.department,
        is_active=True
    )
    
    for staff_member in staff:
        create_notification(
            recipient=staff_member,
            notification_type='approval_pending',
            title='Clearance Awaiting Approval',
            message=f'Student {approval.clearance_request.student.user.get_full_name()} has a clearance request awaiting your department\'s approval.',
            approval=approval,
            clearance=approval.clearance_request,
            send_email=False  # Don't spam staff with emails
        )


def notify_payment_received(payment):
    """
    Notify student and finance staff about payment received
    
    Args:
        payment: Payment object
    """
    # Notify student
    create_notification(
        recipient=payment.student.user,
        notification_type='payment_received',
        title='Payment Received',
        message=f'Your payment of {payment.amount} {payment.currency} has been received. Transaction ID: {payment.transaction_id}. Awaiting verification.',
        payment=payment,
        send_email=True
    )
    
    # Notify finance staff
    from apps.users.models import User
    finance_staff = User.objects.filter(
        role='finance_staff',
        is_active=True
    )
    
    for staff in finance_staff:
        create_notification(
            recipient=staff,
            notification_type='payment_received',
            title='New Payment Received',
            message=f'Payment of {payment.amount} {payment.currency} received from {payment.student.user.get_full_name()}. Awaiting verification.',
            payment=payment,
            send_email=False
        )


def notify_payment_verified(payment):
    """
    Notify student when payment is verified
    
    Args:
        payment: Payment object
    """
    create_notification(
        recipient=payment.student.user,
        notification_type='payment_verified',
        title='Payment Verified',
        message=f'Your payment of {payment.amount} {payment.currency} has been verified. You can now submit your clearance request.',
        payment=payment,
        send_email=True
    )


def notify_payment_failed(payment):
    """
    Notify student when payment fails
    
    Args:
        payment: Payment object
    """
    create_notification(
        recipient=payment.student.user,
        notification_type='payment_received',  # Using payment_received as generic payment notification
        title='Payment Failed',
        message=f'Your payment of {payment.amount} {payment.currency} has failed. Please try again or contact finance office.',
        payment=payment,
        send_email=True
    )
