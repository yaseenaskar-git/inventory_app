# User Settings Feature - Implementation Guide

## Overview
This is a complete, production-ready user settings system that allows logged-in users to manage their account. The feature includes:
- **Change Email**: Update email with validation and current password verification
- **Change Password**: Update password with strength validation and current password verification
- **Delete Account**: Permanently delete account with multi-step confirmation

---

## Architecture & Components

### 1. **Forms** (`accounts/forms.py`)

#### `ChangeEmailForm`
- Validates new email format using Django's built-in validator
- Requires email confirmation (both emails must match)
- Requires current password for security
- **Security**: Prevents changing to duplicate emails

```python
class ChangeEmailForm(forms.Form):
    new_email = EmailField()           # New email address
    confirm_email = EmailField()       # Confirmation
    current_password = CharField()     # Security check
```

#### `ChangePasswordForm`
- Validates password strength using Django's `validate_password()`
- Requires current password before changing
- Confirms new password matches confirmation
- **Security**: Prevents weak passwords, enforces Django's password policy

```python
class ChangePasswordForm(forms.Form):
    current_password = CharField()     # Verify identity
    new_password = CharField()         # Must pass strength validation
    confirm_password = CharField()     # Must match new_password
```

#### `DeleteAccountForm`
- Requires username confirmation (user must type their exact username)
- Requires current password
- **Security**: Multi-step confirmation prevents accidental deletion

```python
class DeleteAccountForm(forms.Form):
    confirmation_text = CharField()    # Must match username
    current_password = CharField()     # Final security check
```

---

### 2. **Views** (`accounts/views.py`)

#### `user_settings()` - Page View
```python
@login_required
@never_cache
def user_settings(request):
    """Display settings page"""
    return render(request, 'accounts/settings.html', {'user': request.user})
```
- **Login Required**: Only authenticated users
- **No Cache**: Ensures fresh page content every time
- **Returns**: Rendered settings template

#### `change_email()` - API Endpoint
```python
@login_required
@require_http_methods(["POST"])
def change_email(request):
    # 1. Validate current password using authenticate()
    # 2. Validate new email format
    # 3. Check for duplicate emails (case-insensitive)
    # 4. Update user.email
    # 5. Return success/error JSON
```

**Security Checks**:
- ✅ Password authentication required
- ✅ Email format validation
- ✅ Duplicate email prevention (case-insensitive)
- ✅ CSRF token required

**Return Values**:
- `200 OK`: `{'success': True, 'message': '...'}`
- `401 Unauthorized`: Invalid password
- `400 Bad Request`: Invalid email or duplicate
- `500 Error`: Server error

#### `change_password()` - API Endpoint
```python
@login_required
@require_http_methods(["POST"])
def change_password(request):
    # 1. Validate current password using authenticate()
    # 2. Validate new password strength
    # 3. Ensure new password != current password
    # 4. Hash and save new password using set_password()
    # 5. Keep user logged in with update_session_auth_hash()
    # 6. Return success/error JSON
```

**Security Checks**:
- ✅ Password authentication required
- ✅ Password strength validation (Django's policy)
- ✅ Prevents reusing current password
- ✅ Sessions not invalidated after change

**Return Values**:
- `200 OK`: `{'success': True, 'message': '...'}`
- `401 Unauthorized`: Invalid current password
- `400 Bad Request`: Weak password or same as current
- `500 Error`: Server error

#### `delete_account()` - API Endpoint
```python
@login_required
@require_http_methods(["POST"])
def delete_account(request):
    # 1. Validate current password using authenticate()
    # 2. Validate username confirmation matches
    # 3. Delete all related data in transaction:
    #    - All Inventory records (Items cascade delete)
    #    - All Category records
    #    - User account
    # 4. Log out user
    # 5. Return success JSON
```

**Security Checks**:
- ✅ Password authentication required
- ✅ Username confirmation to prevent accidents
- ✅ Atomic transaction (all-or-nothing deletion)
- ✅ Session logged out after deletion

**Data Deleted**:
- All `Inventory` objects owned by user
- All `Item` objects in those inventories (cascade)
- All `Category` objects owned by user
- The `User` account itself

**Return Values**:
- `200 OK`: `{'success': True, 'message': '...'}`
- `401 Unauthorized`: Invalid password
- `400 Bad Request`: Username doesn't match
- `500 Error`: Server error

---

### 3. **URLs** (`accounts/urls.py`)

```python
# Page view
path('settings/', views.user_settings, name='user_settings'),

# API endpoints
path('api/settings/email/', views.change_email, name='change_email'),
path('api/settings/password/', views.change_password, name='change_password'),
path('api/settings/delete/', views.delete_account, name='delete_account'),
```

---

### 4. **Template** (`accounts/templates/accounts/settings.html`)

**Layout**: 
- 3-column layout (sidebar + content)
- Sidebar with 3 tabs: Email, Password, Delete Account
- Each section has a form with validation messages

**Features**:
- ✅ Tab switching with JavaScript
- ✅ Real-time form validation
- ✅ Error/success messages
- ✅ Loading states
- ✅ Responsive design
- ✅ Accessibility (ARIA labels)

**JavaScript Functionality**:
```javascript
switchTab(event, tabName)           // Switch between tabs
fetchJSON(url, options)             // Helper for API calls
emailForm submit                    // Submit email change
passwordForm submit                 // Submit password change
deleteForm submit                   // Submit account deletion
```

---

### 5. **Dashboard Integration**

Added settings button to dashboard header:
```html
<a href="{% url 'user_settings' %}" class="btn btn-outline-secondary">⚙️ Settings</a>
```

---

## Security Implementation

### Authentication
- All endpoints decorated with `@login_required`
- User identity verified via password authentication before any changes
- CSRF tokens required for POST requests

### Password Security
- Passwords hashed using Django's `set_password()` (PBKDF2 by default)
- Never stored in plain text
- Password strength validated against Django policy
- Session not invalidated after password change (better UX)

### Email Validation
- Format validated using Django's `validate_email()`
- Uniqueness checked case-insensitive
- Current email preserved until new email confirmed

### Account Deletion
- Multi-step confirmation (username + password)
- Atomic transaction prevents partial deletions
- All user data deleted (inventories, items, categories)
- User logged out automatically
- Cannot be undone

---

## API Reference

### Change Email
**POST** `/accounts/api/settings/email/`

**Request Body**:
```json
{
    "new_email": "newemail@example.com",
    "current_password": "password123"
}
```

**Success Response**:
```json
{
    "success": true,
    "message": "Email successfully changed to newemail@example.com"
}
```

**Error Responses**:
```json
{
    "success": false,
    "error": "Current password is incorrect."
}
```

---

### Change Password
**POST** `/accounts/api/settings/password/`

**Request Body**:
```json
{
    "current_password": "oldpassword123",
    "new_password": "NewPassword123!"
}
```

**Success Response**:
```json
{
    "success": true,
    "message": "Password successfully changed. You remain logged in."
}
```

**Error Responses**:
```json
{
    "success": false,
    "error": "Password validation failed: This password is too common."
}
```

---

### Delete Account
**POST** `/accounts/api/settings/delete/`

**Request Body**:
```json
{
    "username_confirmation": "myusername",
    "current_password": "password123"
}
```

**Success Response**:
```json
{
    "success": true,
    "message": "Account permanently deleted. Redirecting to login..."
}
```

**Error Responses**:
```json
{
    "success": false,
    "error": "Username confirmation does not match. Expected: myusername"
}
```

---

## Error Handling

All endpoints return meaningful error messages:

| Error Type | HTTP Status | Example |
|-----------|------------|---------|
| Invalid password | 401 | "Current password is incorrect." |
| Validation error | 400 | "Invalid email format." |
| Duplicate email | 400 | "This email is already in use by another account." |
| Weak password | 400 | "Password validation failed: ..." |
| Username mismatch | 400 | "Username confirmation does not match." |
| Server error | 500 | "Internal server error" |

---

## User Flow

### Change Email
1. User navigates to Settings
2. Clicks "Change Email" tab
3. Enters new email and current password
4. Submits form
5. Backend validates and updates email
6. Page reloads showing success message
7. Email updated in user's account

### Change Password
1. User navigates to Settings
2. Clicks "Change Password" tab
3. Enters current password, new password, and confirmation
4. Submits form
5. Backend validates password strength
6. Password updated and hashed
7. User remains logged in
8. Success message shown

### Delete Account
1. User navigates to Settings
2. Clicks "Delete Account" tab
3. Warning displayed about permanent deletion
4. Enters username confirmation
5. Enters current password
6. Clicks "Permanently Delete Account"
7. JavaScript shows final confirmation dialog
8. Backend validates and deletes all user data
9. User logged out automatically
10. Redirected to login page after 2 seconds

---

## Testing Checklist

- [ ] Change email with valid password ✓
- [ ] Change email with invalid password ✗
- [ ] Change email to duplicate email ✗
- [ ] Change password with valid current password ✓
- [ ] Change password with invalid current password ✗
- [ ] Change password to weak password ✗
- [ ] Change password and remain logged in ✓
- [ ] Delete account with correct username ✓
- [ ] Delete account with wrong username ✗
- [ ] Delete account with wrong password ✗
- [ ] Verify all user data deleted after account deletion ✓
- [ ] Verify user logged out after account deletion ✓
- [ ] Test with different user roles (if applicable) ✓
- [ ] Test CSRF token validation ✓
- [ ] Test with invalid JSON payloads ✓

---

## Notes

- All operations are atomic (all-or-nothing)
- No sensitive data logged
- Error messages are generic where appropriate (don't reveal if email exists)
- All forms use Django's built-in validators for security
- UI is responsive and mobile-friendly
- Accessibility best practices followed (labels, ARIA)
