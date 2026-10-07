from django.core.management.base import BaseCommand
from baking.models import Category, BakeryItem, CarouselSlide


class Command(BaseCommand):
    help = "Seeds the database with default catalog categories, menu items, and hero carousel slides."

    def handle(self, *args, **options):
        self.stdout.write("Seeding carousel and catalog data...")

        # 1. Seed Carousel Slides
        slides_data = [
            {
                "title": "Bespoke Celebration Cakes",
                "subtitle": "Handcrafted multi-tiered cakes tailored for weddings, birthdays, and milestones.",
                "image_url": "https://images.unsplash.com/photo-1535141192574-5d4897c13136?q=80&w=1200&auto=format&fit=crop",
                "button_text": "Request Custom Cake",
                "button_link": "/custom-order/",
                "order": 1,
            },
            {
                "title": "Gourmet Artisan Cupcakes",
                "subtitle": "Freshly baked daily with real butter, vanilla bean, and Belgian chocolate frosting.",
                "image_url": "https://images.unsplash.com/photo-1576618148400-f54bed99fcfd?q=80&w=1200&auto=format&fit=crop",
                "button_text": "Explore Menu",
                "button_link": "/catalog/",
                "order": 2,
            },
            {
                "title": "Fresh Pastries & Morning Bakes",
                "subtitle": "Glazed cinnamon rolls, butter croissants, and sweet treats in Middelburg.",
                "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=1200&auto=format&fit=crop",
                "button_text": "Order Pastries",
                "button_link": "/catalog/",
                "order": 3,
            },
        ]

        for slide in slides_data:
            CarouselSlide.objects.get_or_create(title=slide["title"], defaults=slide)

        # 2. Seed Categories
        categories_data = [
            {"name": "Celebration Cakes", "slug": "celebration-cakes", "description": "Custom party cakes."},
            {"name": "Artisan Cupcakes", "slug": "artisan-cupcakes", "description": "Single-serve piped cupcakes."},
            {"name": "Daily Pastries", "slug": "daily-pastries", "description": "Fresh morning treats."},
        ]

        cat_objs = {}
        for cat in categories_data:
            obj, _ = Category.objects.get_or_create(slug=cat["slug"], defaults=cat)
            cat_objs[cat["slug"]] = obj

        # 3. Seed Catalog Items with Photos
        items_data = [
            {
                "category_slug": "celebration-cakes",
                "name": "Signature Red Velvet Cake",
                "slug": "signature-red-velvet-cake",
                "description": "Moist red velvet sponge layers topped with cream cheese frosting and gold accents.",
                "price": 480.00,
                "image_url": "https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?q=80&w=800&auto=format&fit=crop",
            },
            {
                "category_slug": "celebration-cakes",
                "name": "Triple Chocolate Fudge Cake",
                "slug": "triple-chocolate-fudge-cake",
                "description": "Rich dark chocolate sponge layered with Belgian chocolate ganache.",
                "price": 520.00,
                "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?q=80&w=800&auto=format&fit=crop",
            },
            {
                "category_slug": "artisan-cupcakes",
                "name": "Buttercream Cupcake Box (6-Pack)",
                "slug": "buttercream-cupcake-box-6",
                "description": "Assorted vanilla bean, chocolate fudge, and salted caramel cupcakes.",
                "price": 180.00,
                "image_url": "https://images.unsplash.com/photo-1519869325930-281384150729?q=80&w=800&auto=format&fit=crop",
            },
            {
                "category_slug": "daily-pastries",
                "name": "Glazed Cinnamon Roll Platter",
                "slug": "cinnamon-roll-platter",
                "description": "Warm, freshly baked cinnamon rolls glazed with rich cream cheese frosting.",
                "price": 220.00,
                "image_url": "https://images.unsplash.com/photo-1509365465985-25d11c17e812?q=80&w=800&auto=format&fit=crop",
            },
        ]

        for item_info in items_data:
            cat_slug = item_info.pop("category_slug")
            image_url = item_info.pop("image_url")
            category = cat_objs.get(cat_slug)
            
            BakeryItem.objects.get_or_create(
                slug=item_info["slug"],
                defaults={**item_info, "category": category, "image": image_url}
            )

        self.stdout.write(self.style.SUCCESS("Catalog & Carousel seeding complete!"))