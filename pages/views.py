from django.shortcuts import render
from properties.models import Property, Category


def home(request):
    featured_properties = Property.objects.filter(
        is_featured=True,
        is_available=True
    )[:6]

    categories = Category.objects.all()

    context = {
        'featured_properties': featured_properties,
        'categories': categories
    }

    return render(request, 'home.html', context)