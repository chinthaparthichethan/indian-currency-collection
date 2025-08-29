from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.db import models  # Add this import
from .models import CurrencyItem
from .forms import CurrencyItemForm, SearchFilterForm

def home(request):
    # Get latest items that have at least one image
    latest_items = CurrencyItem.objects.filter(
        Q(front_image__isnull=False) | 
        Q(image__isnull=False)
    )[:6]
    
    # If no items with images, get all items (for placeholder display)
    if not latest_items.exists():
        latest_items = CurrencyItem.objects.all()[:6]
        
    return render(request, 'index.html', {'latest_items': latest_items})

def gallery(request):
    form = SearchFilterForm(request.GET)
    items = CurrencyItem.objects.all()
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        item_type = form.cleaned_data.get('item_type')
        year_from = form.cleaned_data.get('year_from')
        year_to = form.cleaned_data.get('year_to')
        
        if search:
            items = items.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(denomination__icontains=search)
            )
        
        if item_type:
            items = items.filter(item_type=item_type)
            
        if year_from:
            items = items.filter(year__gte=year_from)
            
        if year_to:
            items = items.filter(year__lte=year_to)
    
    return render(request, 'gallery.html', {'items': items, 'form': form})

def item_detail(request, pk):
    item = get_object_or_404(CurrencyItem, pk=pk)
    return render(request, 'detail.html', {'item': item})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# Admin Views
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'admin/login.html')

@login_required
def admin_dashboard(request):
    items = CurrencyItem.objects.all()
    return render(request, 'admin/dashboard.html', {'items': items})

@login_required
def add_item(request):
    if request.method == 'POST':
        form = CurrencyItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfully!')
            return redirect('admin_dashboard')
    else:
        form = CurrencyItemForm()
    return render(request, 'admin/add_item.html', {'form': form})

@login_required
def edit_item(request, pk):
    item = get_object_or_404(CurrencyItem, pk=pk)
    if request.method == 'POST':
        form = CurrencyItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('admin_dashboard')
    else:
        form = CurrencyItemForm(instance=item)
    return render(request, 'admin/edit_item.html', {'form': form, 'item': item})

@login_required
def delete_item(request, pk):
    item = get_object_or_404(CurrencyItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
    return redirect('admin_dashboard')

def admin_logout(request):
    logout(request)
    return redirect('home')
