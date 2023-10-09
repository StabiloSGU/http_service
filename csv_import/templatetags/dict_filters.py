from django import template

register = template.Library()

@register.filter
def dict_filter(d: dict, key):
    if key in d:
        return d[key]
    else:
        return ''
