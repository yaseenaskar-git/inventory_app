"""
Custom password validators for the application.
Enforces strong password requirements:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character
"""

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class StrongPasswordValidator:
    """
    Custom password validator that enforces strong password requirements.
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter (A-Z)
    - At least one lowercase letter (a-z)
    - At least one digit (0-9)
    - At least one special character (!@#$%^&*)
    """
    
    def validate(self, password, user=None):
        """
        Validate password strength.
        
        Args:
            password: The password to validate
            user: The user object (optional)
            
        Raises:
            ValidationError: If password doesn't meet requirements
        """
        errors = []
        
        # Check minimum length
        if len(password) < 8:
            errors.append(_('Password must be at least 8 characters long.'))
        
        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            errors.append(_('Password must contain at least one uppercase letter (A-Z).'))
        
        # Check for lowercase letter
        if not re.search(r'[a-z]', password):
            errors.append(_('Password must contain at least one lowercase letter (a-z).'))
        
        # Check for digit
        if not re.search(r'[0-9]', password):
            errors.append(_('Password must contain at least one digit (0-9).'))
        
        # Check for special character
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            errors.append(_('Password must contain at least one special character (!@#$%^&*).'))
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        """Return help text describing password requirements."""
        return _(
            'Your password must contain: '
            'at least 8 characters, '
            'an uppercase letter, '
            'a lowercase letter, '
            'a digit, '
            'and a special character.'
        )
