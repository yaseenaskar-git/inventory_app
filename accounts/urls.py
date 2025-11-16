from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/inventories/create/', views.create_inventory, name='create_inventory'),
    path('inventories/<int:inventory_id>/update/', views.update_inventory, name='update_inventory'),
    path('inventories/<int:inventory_id>/delete/', views.delete_inventory, name='delete_inventory'),
    # Inventory item pages and APIs
    path('inventories/<int:inventory_id>/items/', views.ItemListView.as_view(), name='inventory_items'),
    path('inventories/<int:inventory_id>/items/create/', views.ItemCreateView.as_view(), name='create_item'),
    path('inventories/<int:inventory_id>/items/<int:item_id>/update/', views.ItemUpdateView.as_view(), name='update_item'),
    path('inventories/<int:inventory_id>/items/<int:item_id>/delete/', views.ItemDeleteView.as_view(), name='delete_item'),
    path('inventories/<int:inventory_id>/items/<int:item_id>/quantity/', views.item_quantity_update, name='item_quantity_update'),
    path('inventories/<int:inventory_id>/items/<int:item_id>/detail/', views.item_detail_api, name='item_detail_api'),
    path('inventories/<int:inventory_id>/bulk/', views.bulk_action, name='bulk_action'),
    path('categories/create/', views.create_category, name='create_category'),
]
