# post_extras.py
from django import template

register = template.Library()

@register.filter
def return_item(l:list, index:int):
    try:
        return l[index]
    except:
        return None