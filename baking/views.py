from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import BakeryItem, CustomOrderRequest, CarouselSlide
from .forms import CustomOrderForm

def home(request):
    slides = CarouselSlide.objects.filter(is_active=True)
    featured_items = BakeryItem.objects.filter(is_available=True)[:6]
    return render(request, 'baking/home.html', {
        'slides': slides,
        'featured_items': featured_items
    })


def catalog(request):
    items = BakeryItem.objects.filter(is_available=True)
    return render(request, 'baking/catalog.html', {'items': items})


def custom_order(request):
    if request.method == 'POST':
        form = CustomOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            messages.success(request, f"Your order enquiry #{order.id} was submitted successfully!")
            return redirect('baking:order_success', order_id=order.id)
    else:
        form = CustomOrderForm()
    
    return render(request, 'baking/custom_order.html', {'form': form})


def order_success(request, order_id):
    order = get_object_or_404(CustomOrderRequest, id=order_id)
    return render(request, 'baking/order_success.html', {'order': order})