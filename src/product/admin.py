from django.contrib import admin
from .models import Variant, ProductVariant, ProductVariantPrice
# Register your models here.

admin.site.register(Variant)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)