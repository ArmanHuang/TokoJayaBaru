from django import template
from django.templatetags.static import static

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    # Pastikan dictionary bukan None
    if not dictionary:
        return static('images/default.png')
    # Ambil nilai, jika None atau kosong, pakai default
    value = dictionary.get(key)
    if not value:
        return static('images/default.png')
    return value
