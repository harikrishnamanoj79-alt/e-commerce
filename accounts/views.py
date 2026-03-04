from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import Profile

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Update profile fields
        user.profile.phone = phone
        user.profile.address = address
        user.profile.save()

        login(request, user)
        return redirect('home')

    return render(request, 'register.html')





def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 If agent → go to agent dashboard
            if hasattr(user, 'profile') and user.profile.is_agent:
                return redirect('agent_dashboard')

            # Normal user
            return redirect('home')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')






from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from properties.models import Property
from bookings.models import VisitBooking


@login_required
def agent_dashboard(request):

    # Only allow agents
    if not request.user.profile.is_agent:
        return redirect('home')

    # Agent properties
    properties = Property.objects.filter(agent=request.user)

    # Bookings for agent's properties
    bookings = VisitBooking.objects.filter(property__agent=request.user)

    context = {
        'properties': properties,
        'total_properties': properties.count(),
        'total_bookings': bookings.count(),
        'recent_bookings': bookings.order_by('-created_at')[:5]
    }

    return render(request, 'agent_dashboard.html', context)





from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from properties.models import Property, Category
from accounts.models import Profile
from bookings.models import VisitBooking


@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect('home')

    total_properties = Property.objects.count()
    total_available = Property.objects.filter(is_available=True).count()
    total_categories = Category.objects.count()
    total_agents = Profile.objects.filter(is_agent=True).count()
    total_bookings = VisitBooking.objects.count()

    context = {
        'total_properties': total_properties,
        'total_available': total_available,
        'total_categories': total_categories,
        'total_agents': total_agents,
        'total_bookings': total_bookings,
    }

    return render(request, 'admin_dashboard.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from properties.models import Category, Property


@login_required
def admin_categories(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == "POST":
        name = request.POST.get('name')
        Category.objects.create(name=name, slug=name.lower().replace(" ", "-"))
        return redirect('admin_categories')

    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


from django.contrib.auth.models import User
from properties.models import Property
from bookings.models import VisitBooking
from accounts.models import Profile

@login_required
def admin_agents(request):
    if not request.user.is_superuser:
        return redirect('home')

    agents = User.objects.filter(profile__is_agent=True)

    agent_data = []

    for agent in agents:
        properties_count = Property.objects.filter(agent=agent).count()
        bookings_count = VisitBooking.objects.filter(property__agent=agent).count()

        agent_data.append({
            'user': agent,
            'properties_count': properties_count,
            'bookings_count': bookings_count
        })

    return render(request, 'manage_agents.html', {
        'agent_data': agent_data
    })

@login_required
def admin_properties(request):
    if not request.user.is_superuser:
        return redirect('home')

    properties = Property.objects.all()
    return render(request, 'properties.html', {'properties': properties})


from properties.models import SpecificationField, PropertySpecification



@login_required
def admin_spec_fields(request):

    if not request.user.is_superuser:
        return redirect('home')

    categories = Category.objects.all()

    if request.method == "POST":
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        field_type = request.POST.get('field_type')

        SpecificationField.objects.create(
            category_id=category_id,
            name=name,
            field_type=field_type
        )

        return redirect('admin_spec_fields')

    fields = SpecificationField.objects.select_related('category')

    return render(request, 'spec_fields.html', {
        'fields': fields,
        'categories': categories
    })


from properties.models import Property, SpecificationField, PropertySpecification
@login_required
def admin_add_property_spec(request):

    if not request.user.is_superuser:
        return redirect('home')

    properties = Property.objects.all()
    fields = SpecificationField.objects.select_related('category')

    if request.method == "POST":

        property_id = request.POST.get('property')
        field_id = request.POST.get('field')

        if not property_id or not field_id:
            return redirect('admin_add_property_spec')

        property_instance = Property.objects.get(id=property_id)
        spec_field = SpecificationField.objects.get(id=field_id)

        # 🔥 Prevent duplicate spec for same property
        spec, created = PropertySpecification.objects.get_or_create(
            property=property_instance,
            field=spec_field
        )

        if spec_field.field_type == "text":
            spec.value_text = request.POST.get('value_text')

        elif spec_field.field_type == "number":
            spec.value_number = request.POST.get('value_number')

        elif spec_field.field_type == "boolean":
            spec.value_boolean = True if request.POST.get('value_boolean') == "on" else False

        spec.save()

        return redirect('admin_property_specs')

    return render(request, 'add_property_spec.html', {
        'properties': properties,
        'fields': fields
    })
    
    




from properties.models import Property,Category,SpecificationField,PropertySpecification,PropertyImage


@login_required
def admin_add_property(request):

    if not request.user.is_superuser:
        return redirect('home')

    if request.method == "POST":

        # 🔥 Create property
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
            is_available=True
        )

        # 🔥 Save Dynamic Specification Fields
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

        # 🔥 Save Multiple Gallery Images
        gallery_images = request.FILES.getlist('gallery_images')

        for img in gallery_images:
            PropertyImage.objects.create(
                property=property_instance,
                image=img
            )

        return redirect('admin_properties')

    return render(request, 'add_property.html', {
        'categories': Category.objects.all()
    })
    
    
from django.shortcuts import get_object_or_404
from properties.models import Property, Category, SpecificationField, PropertySpecification


@login_required
def admin_edit_property(request, pk):

    if not request.user.is_superuser:
        return redirect('home')

    property_instance = get_object_or_404(Property, pk=pk)
    categories = Category.objects.all()

    if request.method == "POST":

        property_instance.title = request.POST.get('title')
        property_instance.slug = request.POST.get('slug')
        property_instance.description = request.POST.get('description')
        property_instance.price = request.POST.get('price')
        property_instance.location = request.POST.get('location')
        property_instance.category_id = request.POST.get('category')
        property_instance.listing_type = request.POST.get('listing_type')
        property_instance.bedrooms = request.POST.get('bedrooms') or 0
        property_instance.bathrooms = request.POST.get('bathrooms') or 0
        property_instance.area = request.POST.get('area') or 0

        if request.FILES.get('featured_image'):
            property_instance.featured_image = request.FILES.get('featured_image')

        property_instance.save()

        # 🔥 Delete old specifications
        PropertySpecification.objects.filter(property=property_instance).delete()

        # 🔥 Save new specifications
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

        # 🔥 Save additional gallery images
        gallery_images = request.FILES.getlist('gallery_images')
        for img in gallery_images:
            PropertyImage.objects.create(
                property=property_instance,
                image=img
            )

        return redirect('admin_properties')

    return render(request, 'edit_property.html', {
        'property': property_instance,
        'categories': categories
    })
    
    
@login_required
def admin_delete_property(request, pk):

    if not request.user.is_superuser:
        return redirect('home')

    property_instance = get_object_or_404(Property, pk=pk)

    if request.method == "POST":
        property_instance.delete()
        messages.success(request, "Property deleted successfully.")
        return redirect('admin_properties')

    return redirect('admin_properties')

@login_required
def remove_agent_role(request, user_id):

    if not request.user.is_superuser:
        return redirect('home')

    user = User.objects.get(id=user_id)
    user.profile.is_agent = False
    user.profile.save()

    return redirect('admin_agents')

@login_required
def delete_agent(request, user_id):

    if not request.user.is_superuser:
        return redirect('home')

    user = User.objects.get(id=user_id)
    user.delete()

    return redirect('admin_agents')



def agent_detail(request, username):

    # Get agent
    agent_user = get_object_or_404(
        User,
        username=username,
        profile__is_agent=True
    )

    # Get agent properties
    properties = Property.objects.filter(
        agent=agent_user
    )

    # 🔥 Get bookings for agent properties
    bookings = VisitBooking.objects.filter(
        property__agent=agent_user
    ).order_by('-created_at')

    return render(request, 'agent_detail.html', {
        'agent_user': agent_user,
        'properties': properties,
        'bookings': bookings
    })
    
    
@login_required
def admin_delete_spec_field(request, pk):

    if not request.user.is_superuser:
        return redirect('home')

    field = SpecificationField.objects.get(pk=pk)
    field.delete()

    return redirect('admin_spec_fields')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from properties.models import PropertySpecification


@login_required
def admin_property_specs(request):

    # 🔒 Only super admin allowed
    if not request.user.is_superuser:
        return redirect('home')

    # 🔥 Get all property specifications with related data
    specs = PropertySpecification.objects.select_related(
        'property',
        'field',
        'field__category'
    ).order_by('property')

    context = {
        'specs': specs
    }

    return render(request, 'property_specs.html', context)


from bookings.models import VisitBooking

@login_required
def profile_view(request):

    user = request.user
    profile = user.profile

    # 🔹 User booking history
    bookings = VisitBooking.objects.filter(user=user).select_related('property').order_by('-created_at')

    if request.method == "POST":

        user.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')

        if request.FILES.get('image'):
            profile.image = request.FILES.get('image')

        user.save()
        profile.save()

        return redirect('profile')

    return render(request, 'profile.html', {
        'profile': profile,
        'bookings': bookings
    })