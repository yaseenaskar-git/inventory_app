from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Inventory


class RegisterForm(UserCreationForm):
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

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
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

