from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from properties.models import Property
from .models import VisitBooking


@login_required
def book_visit(request, slug):

    property = get_object_or_404(Property, slug=slug)

    if request.method == "POST":

        visit_date = request.POST.get('visit_date')
        message = request.POST.get('message')
        phone = request.POST.get('phone')

        VisitBooking.objects.create(
            property=property,
            user=request.user,   # 🔥 link booking to logged user
            name=request.user.username,
            email=request.user.email,
            phone=phone,
            visit_date=visit_date,
            message=message
        )

        return redirect('property_detail', slug=slug)

    return redirect('property_detail', slug=slug)