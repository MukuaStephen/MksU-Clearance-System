"""
Test script for registration number parsing and validation
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.students.models import Student, validate_registration_number
from django.core.exceptions import ValidationError

def test_validator():
    """Test the registration number validator"""
    print("Testing Registration Number Validator")
    print("=" * 50)
    
    # Valid formats
    valid_cases = [
        "SCE/CS/0001/2024",
        "SBS/ACC/0123/2023",
        "SHSS/PSY/9999/2025",
    ]
    
    print("\n✓ Valid formats:")
    for reg_no in valid_cases:
        try:
            validate_registration_number(reg_no)
            print(f"  {reg_no} → Valid")
        except ValidationError as e:
            print(f"  {reg_no} → Error: {e}")
    
    # Invalid formats
    invalid_cases = [
        "SCE-CS-0001-2024",  # Wrong separators
        "SCE/CS/001/2024",   # Not enough digits
        "sce/cs/0001/2024",  # Lowercase
        "SCE/CS/0001",       # Missing year
        "0001/2024",         # Missing school/dept
    ]
    
    print("\n✗ Invalid formats (should fail):")
    for reg_no in invalid_cases:
        try:
            validate_registration_number(reg_no)
            print(f"  {reg_no} → Valid (UNEXPECTED!)")
        except ValidationError as e:
            print(f"  {reg_no} → Rejected ✓")

def test_parser():
    """Test the registration number parser"""
    print("\n\nTesting Registration Number Parser")
    print("=" * 50)
    
    # Create a mock student object (not saved)
    from apps.users.models import User
    
    test_cases = [
        "SCE/CS/0001/2024",
        "SBS/ACC/0123/2023",
        "SHSS/PSY/9999/2025",
    ]
    
    for reg_no in test_cases:
        # Create temporary student object to test parsing
        student = Student(registration_number=reg_no)
        parsed = student.parse_registration_number()
        
        if parsed:
            print(f"\n{reg_no}:")
            print(f"  School Code: {parsed['school_code']}")
            print(f"  Department Code: {parsed['department_code']}")
            print(f"  Sequence: {parsed['sequence']}")
            print(f"  Admission Year: {parsed['admission_year']}")
        else:
            print(f"\n{reg_no}: Failed to parse")

if __name__ == "__main__":
    test_validator()
    test_parser()
    print("\n" + "=" * 50)
    print("✓ All tests completed")
