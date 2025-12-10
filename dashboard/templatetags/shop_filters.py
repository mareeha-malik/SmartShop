from django import template

register = template.Library()

@register.filter(name="format_price")
def format_price(value):
    """
    Format a numeric price with thousands separator and two decimals.
    Example: 1200 -> '1,200.00'
    """
    try:
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return value
