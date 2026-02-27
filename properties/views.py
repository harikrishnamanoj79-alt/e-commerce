from django.shortcuts import render
from .models import Property,Category
from django.shortcuts import render, get_object_or_404



def property_list(request):
    properties = Property.objects.filter(is_available=True)
    categories = Category.objects.all()

    # 🔍 Location filter
    location = request.GET.get('location')
    if location:
        properties = properties.filter(location__icontains=location)

    # 🏷 Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        properties = properties.filter(category__slug=category_slug)

    context = {
        'properties': properties,
        'categories': categories
    }

    return render(request, 'property_list.html', context)

def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug)
    return render(request, 'property_detail.html', {'property': property})