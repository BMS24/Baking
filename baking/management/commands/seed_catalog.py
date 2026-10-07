from django.core.management.base import BaseCommand
from baking.models import Category, BakeryItem, CarouselSlide


class Command(BaseCommand):
    help = "Seeds the database with default catalog categories, menu items, and hero carousel slides."

    def handle(self, *args, **options):
        self.stdout.write("Seeding catalog and cinnamon roll flyer data...")

        # 1. Seed Carousel Slides
        slides_data = [
            {
                "title": "Freshly Baked Cinnamon Rolls",
                "subtitle": "Freshly baked with your sweet tooth in mind — Oreo, Biscoff, Caramel, and Traditional.",
                "image_url": "https://images.unsplash.com/photo-1509365465985-25d11c17e812?q=80&w=1200&auto=format&fit=crop",
                "button_text": "Order Cinnamon Rolls",
                "button_link": "/catalog/",
                "order": 1,
            },
            {
                "title": "Bespoke Celebration Cakes",
                "subtitle": "Handcrafted multi-tiered cakes tailored for weddings, birthdays, and milestones.",
                "image_url": "https://images.unsplash.com/photo-1535141192574-5d4897c13136?q=80&w=1200&auto=format&fit=crop",
                "button_text": "Request Custom Cake",
                "button_link": "/custom-order/",
                "order": 2,
            },
        ]

        for slide in slides_data:
            CarouselSlide.objects.get_or_create(title=slide["title"], defaults=slide)

        # 2. Seed Categories (All categories explicitly registered)
        categories_data = [
            {
                "name": "Cinnamon Rolls",
                "slug": "cinnamon-rolls",
                "description": "Freshly baked cinnamon rolls with signature cream cheese toppings and gourmet drizzles."
            },
            {
                "name": "Scones",
                "slug": "scones",
                "description": "Freshly baked golden scones packed for gatherings and afternoon teas."
            },
            {
                "name": "Biscuits & Cookies",
                "slug": "biscuits-and-cookies",
                "description": "Handcrafted biscuits and cookies baked in bulk packages."
            },
        ]

        cat_objs = {}
        for cat in categories_data:
            obj, _ = Category.objects.get_or_create(slug=cat["slug"], defaults=cat)
            cat_objs[cat["slug"]] = obj

        # 3. Seed Catalog Items
        items_data = [
            # --- CINNAMON ROLLS ---
            {
                "category_slug": "cinnamon-rolls",
                "name": "Cinnamon Rolls Box of 4 (Assorted)",
                "slug": "cinnamon-rolls-box-of-4",
                "description": "A delicious box of 4 freshly baked cinnamon rolls featuring signature cream cheese topping, drizzled toppings, and crushed crumbs.",
                "price": 40.00,
                "is_available": True,
            },
            {
                "category_slug": "cinnamon-rolls",
                "name": "Oreo Cinnamon Roll",
                "slug": "oreo-cinnamon-roll",
                "description": "Freshly baked roll with rich cream cheese topping, dark chocolate drizzle, and crushed Oreos.",
                "price": 20.00,
                "is_available": True,
            },
            {
                "category_slug": "cinnamon-rolls",
                "name": "Biscoff Cinnamon Roll",
                "slug": "biscoff-cinnamon-roll",
                "description": "Freshly baked roll with signature cream cheese topping, Lotus Biscoff drizzle, and crushed Biscoff biscuit.",
                "price": 20.00,
                "is_available": True,
            },
            {
                "category_slug": "cinnamon-rolls",
                "name": "Caramel Cinnamon Roll",
                "slug": "caramel-cinnamon-roll",
                "description": "Freshly baked roll topped with smooth cream cheese, caramel drizzle, and crushed caramel crunch.",
                "price": 20.00,
                "is_available": True,
            },
            {
                "category_slug": "cinnamon-rolls",
                "name": "Traditional Cinnamon Roll with Chocolate",
                "slug": "traditional-cinnamon-roll-chocolate",
                "description": "Classic cinnamon roll topped with cream cheese glaze and rich chocolate drizzle.",
                "price": 20.00,
                "is_available": True,
            },
            {
                "category_slug": "cinnamon-rolls",
                "name": "Plain Traditional Cinnamon Roll",
                "slug": "plain-traditional-cinnamon-roll",
                "description": "Classic freshly baked roll served with signature cream cheese topping only.",
                "price": 15.00,
                "is_available": True,
            },
            {
                "category_slug": "scones",
                "name": "Scones 1.5L Package",
                "slug": "scones-1-5l-package",
                "description": "Freshly baked traditional scones packaged in a 1.5-liter bucket.",
                "price": 200.00,
                "is_available": True,
            },
            {
                "category_slug": "biscuits-and-cookies",
                "name": "1.5L Biscuit & Cookie Package",
                "slug": "1-5l-biscuit-cookie-package",
                "description": "Assorted freshly baked biscuits and cookies in a 1.5-liter bucket.",
                "price": 180.00,
                "is_available": True,
            },
        ]

        for item_info in items_data:
            cat_slug = item_info.pop("category_slug")
            category = cat_objs.get(cat_slug)
            
            item, created = BakeryItem.objects.get_or_create(
                slug=item_info["slug"],
                defaults={**item_info, "category": category}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added item: {item.name} (R{item.price})"))
            else:
                self.stdout.write(f"Updated item: {item.name}")

        self.stdout.write(self.style.SUCCESS("Database catalog successfully updated!"))