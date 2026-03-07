from django.shortcuts import render
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import re
from django.shortcuts import render
from django.db.models import Q
from .models import Property, Category



import re
import re
from django.db.models import Q
from django.shortcuts import render
from .models import Property, Category


def property_list(request):

    properties = Property.objects.filter(is_available=True)
    categories = Category.objects.all()

    # -----------------------
    # 🔍 Keyword Search
    # -----------------------
    query = request.GET.get('q')

    if query:

        query_lower = query.lower()

        # search in title & description
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

        # 🔹 bedroom search (3bhk / 3 bedroom)
        bedroom_match = re.search(r'(\d+)\s*(bhk|bedroom)', query_lower)
        if bedroom_match:
            bedrooms = int(bedroom_match.group(1))
            properties = properties.filter(bedrooms=bedrooms)

        # 🔹 price search (under 20000000)
        under_match = re.search(r'under\s*(\d+)', query_lower)
        if under_match:
            price = int(under_match.group(1))
            properties = properties.filter(price__lte=price)

        # 🔹 location search (in kochi)
        if " in " in query_lower:
            location = query_lower.split(" in ")[1]
            properties = properties.filter(location__icontains=location)

    # -----------------------
    # 📍 Location Filter
    # -----------------------

    location = request.GET.get('location')
    if location:
        properties = properties.filter(location__icontains=location)

    # -----------------------
    # 🏷 Category Filter
    # -----------------------

    category_slug = request.GET.get('category')
    if category_slug:
        properties = properties.filter(category__slug=category_slug)

    # -----------------------
    # 💰 Price Filters
    # -----------------------

    min_price = request.GET.get('min_price')
    if min_price:
        properties = properties.filter(price__gte=min_price)

    max_price = request.GET.get('max_price')
    if max_price:
        properties = properties.filter(price__lte=max_price)

    context = {
        'properties': properties,
        'categories': categories,
    }

    return render(request, 'property_list.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Property, PropertySpecification
from bookings.models import VisitBooking


def property_detail(request, slug):

    property = get_object_or_404(Property, slug=slug)

    # 🔥 get property specifications
    specs = PropertySpecification.objects.filter(property=property).select_related('field')

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        visit_date = request.POST.get('visit_date')
        message = request.POST.get('message')

        VisitBooking.objects.create(
            property=property,
            name=name,
            email=email,
            phone=phone,
            visit_date=visit_date,
            message=message
        )

        messages.success(request, "Visit booking submitted successfully!")
        return redirect('property_detail', slug=slug)

    return render(request, 'property_detail.html', {
        'property': property,
        'specs': specs
    })




@login_required
def agent_add_property(request):

    if not request.user.profile.is_agent:
        return redirect('home')

    if request.method == "POST":

        # 1️⃣ Create Property and store instance
        property_instance = Property.objects.create(
            title=request.POST.get('title'),
            slug=request.POST.get('slug'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            location=request.POST.get('location'),
            category_id=request.POST.get('category'),
            listing_type=request.POST.get('listing_type'),
            bedrooms=request.POST.get('bedrooms') or 0,
            bathrooms=request.POST.get('bathrooms') or 0,
            area=request.POST.get('area') or 0,
            featured_image=request.FILES.get('featured_image'),
            agent=request.user
        )

        # 2️⃣ Save dynamic specification values
        for key, value in request.POST.items():

            if key.startswith("spec_"):

                field_id = key.split("_")[1]
                spec_field = SpecificationField.objects.get(id=field_id)

                spec = PropertySpecification(
                    property=property_instance,
                    field=spec_field
                )

                if spec_field.field_type == "text":
                    spec.value_text = value

                elif spec_field.field_type == "number":
                    spec.value_number = value

                elif spec_field.field_type == "boolean":
                    spec.value_boolean = True if value == "on" else False

                spec.save()

        messages.success(request, "Property added successfully!")
        return redirect('agent_dashboard')

    return render(request, 'agent_add_property.html', {
        'categories': Category.objects.all()
    })
    



from django.http import JsonResponse
from .models import SpecificationField


def get_category_specifications(request):

    category_id = request.GET.get('category_id')

    # If no category selected, return empty list
    if not category_id:
        return JsonResponse({'fields': []})

    fields = SpecificationField.objects.filter(category_id=category_id)

    data = []

    for field in fields:
        data.append({
            'id': field.id,
            'name': field.name,
            'type': field.field_type
        })

    return JsonResponse({'fields': data})


from django.http import JsonResponse
from django.db.models import Q
from .models import Property, Category


def search_suggestions(request):

    query = request.GET.get("q", "")

    suggestions = []

    if query:

        # Property titles
        properties = Property.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query)
        )[:5]

        for p in properties:
            suggestions.append(p.title)

        # Categories
        categories = Category.objects.filter(
            name__icontains=query
        )[:3]

        for c in categories:
            suggestions.append(c.name)

    return JsonResponse(suggestions, safe=False)