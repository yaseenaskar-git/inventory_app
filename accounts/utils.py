from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def user_is_authenticated(view_func):
    """
    Decorator to ensure user is authenticated.
    Equivalent to @login_required but can be customized.
    """
    return login_required(view_func)


def check_user_inventory_access(user, inventory_id):
    """
    Helper function to check if user has access to a specific inventory.
    Will be used in the inventory feature.
    """
    from django.contrib.auth.models import User
    # Placeholder for future inventory permission logic
    return True
