
from products.models import Product
import json

already_done = [
    'Citrus Peak IPA',
    'Summit Breeze IPA',
    'Golden Trail Lager',
    'Crystal Clear',
    'Basecamp Lager',
    'Summit Chill'
]

products = Product.objects.exclude(name__in=already_done).order_by('category__name', 'name')
batches = {}

for p in products:
    cat = p.category.name if p.category else 'Uncategorized'
    if cat not in batches:
        batches[cat] = []
    batches[cat].append(p.name)

with open('image_generation_plan.txt', 'w', encoding='utf-8') as f:
    for cat, items in batches.items():
        f.write(f"Category: {cat}\n")
        for item in items:
            f.write(f" - {item}\n")
        f.write("\n")
