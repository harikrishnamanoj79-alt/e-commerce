from django.db import models
from django.contrib.auth.models import User
from properties.models import Property


class VisitBooking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='visit_bookings',
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    visit_date = models.DateField()
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else self.name} - {self.property.title}"