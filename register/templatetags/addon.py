from django import template

register = template.Library()

@register.filter
def index(i , n):
    return i[n]