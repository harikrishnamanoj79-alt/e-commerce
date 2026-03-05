import os
import django
import cloudinary
import cloudinary.uploader

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "estatepro.settings")
django.setup()

# Cloudinary configuration
cloudinary.config(
    cloud_name="dxfbrubyj",
    api_key="347828243962665",
    api_secret="2zrrQsBvhGShfFLF8-3wKnetcE4"
)

from properties.models import Property, PropertyImage, Category


def upload_image(image_field):
    if not image_field:
        return

    try:
        file_path = image_field.path

        if os.path.exists(file_path):
            result = cloudinary.uploader.upload(file_path)

            # Store the full secure URL
            image_field.name = result["secure_url"]

            print("Uploaded:", result["secure_url"])

    except Exception as e:
        print("Error uploading:", e)


def migrate():

    for p in Property.objects.all():
        upload_image(p.featured_image)
        p.save()

    for img in PropertyImage.objects.all():
        upload_image(img.image)
        img.save()

    for cat in Category.objects.all():
        upload_image(cat.image)
        cat.save()

    print("Migration complete")


migrate()