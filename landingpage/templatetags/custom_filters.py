from django import template
from django.templatetags.static import static

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key) or static('images/default.png')
