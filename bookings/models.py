from django.db import models
from properties.models import Property

class VisitBooking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    visit_date = models.DateField()
    message = models.TextField(blank=True)

    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.property.title}"