from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Inventory, Item
from .validators import StrongPasswordValidator


class ChangeEmailForm(forms.Form):
    """Form for changing user email address"""
    new_email = forms.EmailField(
        label='New Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new email',
            'required': 'required'
        })
    )
    confirm_email = forms.EmailField(
        label='Confirm Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new email',
            'required': 'required'
        })
    )
    current_password = forms.CharField(
        label='Current Password (for security)',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current password',
            'required': 'required'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get('new_email')
        confirm_email = cleaned_data.get('confirm_email')

        if new_email and confirm_email:
            if new_email != confirm_email:
                raise ValidationError('Email addresses do not match.')

        return cleaned_data


class ChangePasswordForm(forms.Form):
    """Form for changing user password with strength validation"""
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current password',
            'required': 'required'
        })
    )
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new password',
            'required': 'required'
        }),
        help_text=(
            'Password must contain: '
            'at least 8 characters, '
            'an uppercase letter (A-Z), '
            'a lowercase letter (a-z), '
            'a digit (0-9), '
            'and a special character (!@#$%^&*).'
        )
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new password',
            'required': 'required'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError('Passwords do not match.')

        # Validate password strength with custom validator
        if new_password:
            validator = StrongPasswordValidator()
            try:
                validator.validate(new_password)
            except ValidationError as e:
                self.add_error('new_password', e)

        return cleaned_data


class DeleteAccountForm(forms.Form):
    """Form for account deletion confirmation"""
    confirmation_text = forms.CharField(
        label='Type your username to confirm deletion',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type your username here',
            'required': 'required'
        }),
        help_text='This action cannot be undone. All your data will be permanently deleted.'
    )
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password to confirm',
            'required': 'required'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class RegisterForm(forms.Form):
    """Registration form for new users"""
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        help_text=(
            'Password must contain: '
            'at least 8 characters, '
            'an uppercase letter (A-Z), '
            'a lowercase letter (a-z), '
            'a digit (0-9), '
            'and a special character (!@#$%^&*).'
        )
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError('Passwords do not match.')
        
        # Validate password strength with custom validator
        if password:
            validator = StrongPasswordValidator()
            try:
                validator.validate(password)
            except ValidationError as e:
                self.add_error('password', e)
        
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )


class InventoryForm(forms.ModelForm):
    emoji = forms.ChoiceField(
        choices=[
            ('📦', '📦 Box'),
            ('🏠', '🏠 Home'),
            ('🎁', '🎁 Gift'),
            ('📚', '📚 Books'),
            ('🍕', '🍕 Food'),
            ('🛒', '🛒 Shopping'),
            ('💼', '💼 Work'),
            ('🎮', '🎮 Gaming'),
            ('📱', '📱 Electronics'),
            ('👕', '👕 Clothes'),
            ('🎨', '🎨 Art'),
            ('🔧', '🔧 Tools'),
            ('🌱', '🌱 Garden'),
            ('⚽', '⚽ Sports'),
            ('🎵', '🎵 Music'),
            ('📸', '📸 Photos'),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'emoji-selector'
        })
    )

    class Meta:
        model = Inventory
        fields = ('name', 'emoji')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter inventory name',
                'maxlength': '255'
            })
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Inventory name is required.')
        if len(name) > 255:
            raise ValidationError('Inventory name must be less than 255 characters.')
        if self.user and Inventory.objects.filter(user=self.user, name=name).exists():
            raise ValidationError('You already have an inventory with this name.')
        return name




class ItemForm(forms.ModelForm):
    remove_image = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Item
        fields = ('name', 'quantity', 'brand', 'description', 'expiration_date', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand (optional)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description (optional)'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_quantity(self):
        q = self.cleaned_data.get('quantity')
        if q is None:
            return 0
        if q < 0:
            raise ValidationError('Quantity cannot be negative.')
        return q

