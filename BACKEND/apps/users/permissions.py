"""
Custom permission classes for role-based access control
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission class to check if user is an admin
    """
    message = "You must be an administrator to perform this action."
    
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'admin'
        )


class IsDepartmentStaff(permissions.BasePermission):
    """
    Permission class to check if user is department staff
    """
    message = "You must be a department staff member to perform this action."
    
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'department_staff'
        )


class IsStudent(permissions.BasePermission):
    """
    Permission class to check if user is a student
    """
    message = "You must be a student to perform this action."
    
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'student'
        )


class IsAdminOrDepartmentStaff(permissions.BasePermission):
    """
    Permission class to check if user is admin or department staff
    """
    message = "You must be an administrator or department staff to perform this action."
    
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role in ['admin', 'department_staff']
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class to check if user is the owner of the object or an admin
    Object-level permission to only allow owners or admins to edit/view
    """
    message = "You can only access your own data."
    
    def has_object_permission(self, request, view, obj):
        # Admins can access everything
        if request.user.role == 'admin':
            return True
        
        # Check if object has a 'user' attribute (for Student, FinanceRecord, etc.)
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object IS the user (for User model itself)
        if hasattr(obj, 'email'):
            return obj == request.user
        
        return False


class IsStudentOwnerOrAdmin(permissions.BasePermission):
    """
    Permission for student-related objects
    Students can only access their own data, admins can access all
    """
    message = "You can only access your own student data."
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admins can access everything
        if request.user.role == 'admin':
            return True
        
        # Students can only access their own student record
        if request.user.role == 'student':
            # Check if object has a user attribute
            if hasattr(obj, 'user'):
                return obj.user == request.user
            # Check if looking at the student's own clearance
            if hasattr(obj, 'student'):
                return obj.student.user == request.user
        
        return False


class CanApproveClearance(permissions.BasePermission):
    """
    Permission for approving clearances
    Only department-specific staff (for their department) or admins can approve
    """
    message = "You do not have permission to approve this clearance."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in [
                'admin',
                'department_staff',
                'library_staff',
                'finance_staff',
                'hostel_staff',
                'academic_staff',
                'gown_issuance_staff',
                'clearance_officer'
            ]
        )

    def has_object_permission(self, request, view, obj):
        # Admins can approve any clearance
        if request.user.role == 'admin':
            return True

        # Department-specific staff can only approve for their assigned department
        if request.user.role in [
            'department_staff',
            'library_staff',
            'finance_staff',
            'hostel_staff',
            'academic_staff',
            'gown_issuance_staff',
            'clearance_officer'
        ]:
            # Check if user has a department assigned
            if not hasattr(request.user, 'department') or not request.user.department:
                return False

            # obj should be a ClearanceApproval instance
            if hasattr(obj, 'department'):
                # Staff can only approve for their assigned department
                return obj.department == request.user.department

        return False


class ReadOnly(permissions.BasePermission):
    """
    Permission that only allows read operations (GET, HEAD, OPTIONS)
    """
    message = "Read-only access. Modifications are not allowed."
    
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission that allows read access to everyone, 
    but write access only to admins
    """
    message = "Only administrators can modify this resource."
    
    def has_permission(self, request, view):
        # Read permissions for any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions only for admins
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'admin'
        )
