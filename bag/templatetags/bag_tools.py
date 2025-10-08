from django import template


register = template.Library()

@register.simple_tag
def bag_contents(request):
    """Return bag contents for use in templates."""
    from ..contexts import bag_contents as bag_contents_func
    return bag_contents_func(request)

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity
