from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm, LoginForm, InventoryForm
from .models import Inventory
import json


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Inventory Manager.')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
                user_obj = authenticate(request, username=user.username, password=password)
                
                if user_obj is not None:
                    login(request, user_obj)
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    inventories = Inventory.objects.filter(user=request.user)
    return render(request, 'accounts/dashboard.html', {
        'user': request.user,
        'inventories': inventories
    })


@login_required(login_url='login')
@require_http_methods(["POST"])
def create_inventory(request):
    """API endpoint to create a new inventory"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        emoji = data.get('emoji', '📦')

        # Validate input
        if not name:
            return JsonResponse({
                'success': False,
                'error': 'Inventory name is required.'
            }, status=400)

        if len(name) > 255:
            return JsonResponse({
                'success': False,
                'error': 'Inventory name must be less than 255 characters.'
            }, status=400)

        # Check for duplicate
        if Inventory.objects.filter(user=request.user, name=name).exists():
            return JsonResponse({
                'success': False,
                'error': 'You already have an inventory with this name.'
            }, status=400)

        # Create inventory
        inventory = Inventory.objects.create(
            user=request.user,
            name=name,
            emoji=emoji
        )

        return JsonResponse({
            'success': True,
            'message': f'Inventory "{name}" created successfully!',
            'inventory': {
                'id': inventory.id,
                'name': inventory.name,
                'emoji': inventory.emoji
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request format.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
