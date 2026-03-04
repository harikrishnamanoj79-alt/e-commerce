from django.shortcuts import render,redirect
from properties.models import Property, Category
from django.contrib import messages
from .models import ContactMessage



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



def about(request):
    return render(request, 'about.html')


def contact(request):

    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )

        messages.success(request, "Message sent successfully!")
        return redirect('contact')

    return render(request, 'contact.html')

from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)