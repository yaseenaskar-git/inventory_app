from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Item
from .validators import StrongPasswordValidator


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

