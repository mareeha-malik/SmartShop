from django import template
from dashboard.models import Product

register = template.Library()

@register.simple_tag
def total_products():
    return Product.objects.count()
