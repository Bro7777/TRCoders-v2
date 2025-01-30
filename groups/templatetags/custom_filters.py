from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Sözlükten anahtar ile değer döndürür."""
    return dictionary.get(key, '')