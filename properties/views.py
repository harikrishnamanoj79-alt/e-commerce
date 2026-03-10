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


from num2words import num2words
from django.db.models import Q
import re

import re
from django.db.models import Q
from num2words import num2words
from properties.models import Property, Category


def property_list(request):

    properties = Property.objects.filter(is_available=True)
    categories = Category.objects.all()

    # -----------------------
    # 🔍 Smart Keyword Search
    # -----------------------

    query = request.GET.get('q')

    if query:

        query = query.strip()
        query_lower = query.lower()

        # 🔹 Search in multiple fields
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(category__name__icontains=query)
        )

        # -----------------------
        # 🏠 Bedroom search
        # -----------------------

        bedroom_match = re.search(r'(\d+)\s*(bhk|bedroom)', query_lower)

        if bedroom_match:
            bedrooms = int(bedroom_match.group(1))
            properties = properties.filter(bedrooms=bedrooms)

        # -----------------------
        # 💰 Price search
        # -----------------------

        under_match = re.search(r'under\s*(\d+)', query_lower)

        if under_match:
            price = int(under_match.group(1))
            properties = properties.filter(price__lte=price)

        # -----------------------
        # 📍 Location search
        # -----------------------

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
    max_price = request.GET.get('max_price')

    if min_price:
        properties = properties.filter(price__gte=min_price)

    if max_price:
        properties = properties.filter(price__lte=max_price)

    # -----------------------
    # 🔹 Convert price to words
    # -----------------------

    for p in properties:
        p.price_words = num2words(p.price, lang='en_IN').title()

    context = {
        "properties": properties,
        "categories": categories,
        "query": query
    }

    return render(request, "property_list.html", context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Property, PropertySpecification
from bookings.models import VisitBooking


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from num2words import num2words

def property_detail(request, slug):

    property = get_object_or_404(Property, slug=slug)

    # property specifications
    specs = PropertySpecification.objects.filter(property=property).select_related('field')

    # convert price to words
    price_words = num2words(property.price, lang='en_IN').title()

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
        'specs': specs,
        'price_words': price_words
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.text import slugify
from django.utils import timezone
from accounts.views import Profile

@login_required
def agent_add_property(request):

    if not request.user.profile.is_agent:
        return redirect('home')

    owner = None
    phone = request.GET.get('phone')

    # SEARCH OWNER
    if phone:
        owner = Profile.objects.filter(phone=phone).first()

    if request.method == "POST":

        owner_phone = request.POST.get('owner_phone')
        owner_profile = Profile.objects.filter(phone=owner_phone).first()

        if not owner_profile:
            messages.error(request, "Owner not found")
            return redirect('agent_add_property')

        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)

        # Auto slug
        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
        cat_short = slugify(category.name)[:3]
        auto_slug = f"{cat_short}-{timestamp}"

        property_instance = Property.objects.create(
            owner=owner_profile.user,
            title=request.POST.get('title'),
            slug=auto_slug,
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            location=request.POST.get('location'),
            category_id=category_id,
            listing_type=request.POST.get('listing_type'),
            latitude=request.POST.get('latitude'),
            longitude=request.POST.get('longitude'),
            featured_image=request.FILES.get('featured_image'),
            agent=request.user,
            is_available=True
        )

        # Save specifications
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

        # Save gallery
        gallery_images = request.FILES.getlist('gallery_images')

        for img in gallery_images:
            PropertyImage.objects.create(
                property=property_instance,
                image=img
            )

        messages.success(request, "Property added successfully!")
        return redirect('agent_dashboard')

    return render(request, 'agent_add_property.html', {
        'categories': Category.objects.all(),
        'owner': owner,
        'phone': phone
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def agent_edit_property(request, pk):

    property = get_object_or_404(Property, id=pk, agent=request.user)

    if not request.user.profile.is_agent:
        return redirect('home')

    if request.method == "POST":

        property.title = request.POST.get('title')
        property.slug = request.POST.get('slug')
        property.description = request.POST.get('description')
        property.price = request.POST.get('price')
        property.location = request.POST.get('location')
        property.category_id = request.POST.get('category')
        property.listing_type = request.POST.get('listing_type')

        # optional image change
        if request.FILES.get('featured_image'):
            property.featured_image = request.FILES.get('featured_image')

        property.save()

        # save specifications
        for key, value in request.POST.items():

            if key.startswith("spec_"):

                field_id = key.split("_")[1]

                spec_field = SpecificationField.objects.get(id=field_id)

                spec, created = PropertySpecification.objects.get_or_create(
                    property=property,
                    field=spec_field
                )

                if spec_field.field_type == "text":
                    spec.value_text = value

                elif spec_field.field_type == "number":
                    spec.value_number = value

                elif spec_field.field_type == "boolean":
                    spec.value_boolean = True if value == "on" else False

                spec.save()

        # add new gallery images
        gallery_images = request.FILES.getlist('gallery_images')

        for img in gallery_images:
            PropertyImage.objects.create(
                property=property,
                image=img
            )

        messages.success(request, "Property updated successfully")
        return redirect('agent_dashboard')

    return render(request, "agent_edit_property.html", {
        "property": property,
        "categories": Category.objects.all()
    })
    

@login_required
def agent_property_detail(request, pk):

    property = get_object_or_404(
        Property,
        id=pk,
        agent=request.user
    )

    specs = PropertySpecification.objects.filter(property=property)

    return render(request,
        "agent_property_detail.html",
        {
            "property": property,
            "specs": specs
        }
    )
    
    
from django.shortcuts import get_object_or_404

@login_required
def agent_delete_property(request, pk):

    property = get_object_or_404(
        Property,
        id=pk,
        agent=request.user
    )

    property.delete()

    messages.success(request, "Property deleted successfully")

    return redirect("agent_properties")

@login_required
def agent_update_booking(request, booking_id, status):

    booking = get_object_or_404(VisitBooking, id=booking_id)

    if booking.property.agent != request.user:
        return redirect("agent_dashboard")

    booking.status = status
    booking.save()

    return redirect("agent_dashboard")