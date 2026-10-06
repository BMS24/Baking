import os
from django.db import models
from django.utils import timezone
from datetime import timedelta, date
from django.core.exceptions import ValidationError


def min_24h_lead_time(selected_date):
    """Ensures at least 24 hours advance notice is provided."""
    if selected_date < date.today() + timedelta(days=1):
        raise ValidationError("Orders require at least 24 hours advance notice.")


def reference_image_path(instance, filename):
    return f"custom_orders/{date.today().strftime('%Y/%m')}/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default="")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class BakeryItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Set 0.00 for custom quoted items")
    image = models.ImageField(upload_to="catalog/", null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class CustomOrderRequest(models.Model):
    class FulfillmentType(models.TextChoices):
        PICKUP = "PICKUP", "Local Pickup (Middelburg)"
        DELIVERY = "DELIVERY", "Middelburg Suburb Delivery"

    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "Pending Review"
        QUOTED = "QUOTED", "Quoted - Awaiting Payment"
        DEPOSIT_PAID = "DEPOSIT_PAID", "Deposit Paid"
        IN_PREPARATION = "IN_PREPARATION", "In Preparation"
        READY = "READY", "Ready for Pickup / Delivery"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    fulfillment_type = models.CharField(max_length=10, choices=FulfillmentType.choices, default=FulfillmentType.PICKUP)
    delivery_address = models.TextField(blank=True, default="", help_text="Street & Suburb in Middelburg (e.g., Aerorand, Kanonkop)")
    event_date = models.DateField(validators=[min_24h_lead_time])
    
    servings_required = models.PositiveIntegerField(default=12)
    flavor_preference = models.CharField(max_length=200, blank=True, default="")
    dietary_requirements = models.CharField(max_length=200, blank=True, default="", help_text="e.g., Eggless, Nut-free, Gluten-free")
    design_instructions = models.TextField(help_text="Describe theme, colors, or tier details")
    reference_image = models.ImageField(upload_to=reference_image_path, null=True, blank=True)

    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} — {self.customer_name} ({self.event_date})"