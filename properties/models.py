from django.db import models
from django.utils.text import slugify

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Property(models.Model):

    PROPERTY_TYPE = [
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Commercial', 'Commercial'),
        ('Plot', 'Plot'),
    ]

    LISTING_TYPE = [
        ('Sale', 'Sale'),
        ('Rent', 'Rent'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=200)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='properties')
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE)

    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    area = models.IntegerField(help_text="Area in sqft")
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    

    featured_image = models.ImageField(upload_to='properties/')
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_gallery/')

    def __str__(self):
        return self.property.title
    


