from django.shortcuts import render, get_object_or_404
from .models import Category, MenuItem


def menu_list(request):
    categories = Category.objects.prefetch_related('items').all()
    query = request.GET.get('q', '').strip()
    items = MenuItem.objects.filter(is_available=True).select_related('category')
    if query:
        items = items.filter(name__icontains=query)
    context = {
        'categories': categories,
        'items': items,
        'query': query,
    }
    return render(request, 'menu/menu_list.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = category.items.filter(is_available=True)
    categories = Category.objects.all()
    return render(request, 'menu/menu_list.html', {
        'categories': categories,
        'items': items,
        'current_category': category,
    })


def item_detail(request, slug):
    item = get_object_or_404(MenuItem, slug=slug, is_available=True)
    related_items = MenuItem.objects.filter(category=item.category, is_available=True).exclude(id=item.id)[:4]
    return render(request, 'menu/item_detail.html', {'item': item, 'related_items': related_items})
