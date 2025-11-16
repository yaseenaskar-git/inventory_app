from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from .forms import RegisterForm, LoginForm, InventoryForm
from .models import Inventory
import json
from .forms import ItemForm
from .models import Item, Category
from sorl.thumbnail import get_thumbnail

from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.db import transaction


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
@never_cache
def dashboard(request):
    inventories = Inventory.objects.filter(user=request.user)
    return render(request, 'accounts/dashboard.html', {
        'user': request.user,
        'inventories': inventories
    })


@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_inventory(request, inventory_id):
    """Delete an inventory and all its items"""
    try:
        inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)
        # Delete all items first (cascade) then inventory
        Item.objects.filter(inventory_id=inventory_id).delete()
        Inventory.objects.filter(id=inventory_id).delete()
        return JsonResponse({'success': True, 'message': 'Inventory deleted'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def update_inventory(request, inventory_id):
    """Update an inventory"""
    try:
        inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        emoji = data.get('emoji', '📦')
        
        if not name:
            return JsonResponse({'success': False, 'error': 'Name required'}, status=400)
        
        # Check for duplicate name (excluding current inventory)
        if Inventory.objects.filter(user=request.user, name=name).exclude(id=inventory_id).exists():
            return JsonResponse({'success': False, 'error': 'Inventory with this name already exists'}, status=400)
        
        inventory.name = name
        inventory.emoji = emoji
        inventory.save()
        return JsonResponse({'success': True, 'message': 'Inventory updated'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


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


# --------------------
# Items and Categories
# --------------------


class ItemListView(LoginRequiredMixin, View):
    """Display items for a given inventory and handle filtering/searching via query params."""
    login_url = 'login'

    def get(self, request, inventory_id):
        inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)
        items_qs = Item.objects.filter(inventory=inventory)

        # Sorting
        from django.db.models import Case, When, Value
        sort = request.GET.get('sort')
        if sort == 'expiry_asc':
            # Sort soon to late, but items with no expiry date go to the end
            items_qs = items_qs.annotate(
                has_expiry=Case(
                    When(expiration_date__isnull=True, then=Value(1)),
                    default=Value(0)
                )
            ).order_by('has_expiry', 'expiration_date')
        elif sort == 'expiry_desc':
            # Sort late to soon, but items with no expiry date go to the end
            items_qs = items_qs.annotate(
                has_expiry=Case(
                    When(expiration_date__isnull=True, then=Value(1)),
                    default=Value(0)
                )
            ).order_by('has_expiry', '-expiration_date')
        elif sort == 'quantity_asc':
            items_qs = items_qs.order_by('quantity')
        elif sort == 'quantity_desc':
            items_qs = items_qs.order_by('-quantity')

        # Pagination (optional)
        paginator = Paginator(items_qs, 60)
        page = request.GET.get('page')
        items = paginator.get_page(page)

        response = render(request, 'accounts/inventory_items.html', {
            'inventory': inventory,
            'items': items,
        })
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


class ItemCreateView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, inventory_id):
        inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)

        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                item = form.save(commit=False)
                item.inventory = inventory
                item.save()

                # ActivityLog removed

            return JsonResponse({'success': True, 'item': {
                'id': item.id,
                'name': item.name,
                'quantity': item.quantity,
                'category': item.category.name if item.category else None,
                'image_url': item.image.url if item.image else None,
                'thumbnail_url': get_thumbnail(item.image, '300x', quality=85).url if item.image else None,
            }})

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


class ItemUpdateView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, inventory_id, item_id):
        inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)
        item = get_object_or_404(Item, id=item_id, inventory=inventory)

        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            remove_image = form.cleaned_data.get('remove_image')
            with transaction.atomic():
                item = form.save(commit=False)
                if remove_image and item.image:
                    item.image.delete(save=False)
                    item.image = None
                    # ActivityLog removed

                item.save()
                # ActivityLog removed

            return JsonResponse({'success': True, 'item': {
                'id': item.id,
                'name': item.name,
                'quantity': item.quantity,
                'category': item.category.name if item.category else None,
                'image_url': item.image.url if item.image else None,
                'thumbnail_url': get_thumbnail(item.image, '300x', quality=85).url if item.image else None,
            }})

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


class ItemDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, inventory_id, item_id):
        try:
            inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)
            item = get_object_or_404(Item, id=item_id, inventory=inventory)
            item.delete()
            return JsonResponse({'success': True, 'message': 'Item deleted'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def item_quantity_update(request, inventory_id, item_id):
    inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)
    item = get_object_or_404(Item, id=item_id, inventory=inventory)
    try:
        data = json.loads(request.body)
        action = data.get('action')
        amount = int(data.get('amount', 1))
        if action == 'increase':
            item.quantity += amount
            item.save()
            # ActivityLog removed
        elif action == 'decrease':
            item.quantity = max(0, item.quantity - amount)
            item.save()
            # ActivityLog removed
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)

        return JsonResponse({'success': True, 'quantity': item.quantity})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def create_category(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        if not name:
            return JsonResponse({'success': False, 'error': 'Category name required'}, status=400)
        if Category.objects.filter(user=request.user, name__iexact=name).exists():
            return JsonResponse({'success': False, 'error': 'Category already exists'}, status=400)
        cat = Category.objects.create(user=request.user, name=name)
        return JsonResponse({'success': True, 'category': {'id': cat.id, 'name': cat.name}})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required(login_url='login')
def item_detail_api(request, inventory_id, item_id):
    inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)
    item = get_object_or_404(Item, id=item_id, inventory=inventory)
    return JsonResponse({
        'success': True,
        'item': {
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity,
            'brand': item.brand,
            'description': item.description,
            'expiration_date': item.expiration_date.isoformat() if item.expiration_date else None,
            'image_url': item.image.url if item.image else None,
            'thumbnail_url': get_thumbnail(item.image, '300x', quality=85).url if item.image else None,
        }
    })


@login_required(login_url='login')
@require_http_methods(["POST"])
def bulk_action(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)
    try:
        data = json.loads(request.body)
        action = data.get('action')
        item_ids = data.get('item_ids', [])
        amount = int(data.get('amount', 1))
        items = Item.objects.filter(id__in=item_ids, inventory=inventory)
        if action == 'delete':
            items.delete()
            return JsonResponse({'success': True})
        elif action in ['increase', 'decrease']:
            for it in items:
                if action == 'increase':
                    it.quantity += amount
                    # ActivityLog removed
                else:
                    it.quantity = max(0, it.quantity - amount)
                    # ActivityLog removed
                it.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Unknown bulk action'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
