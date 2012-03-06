from django import template
from django.forms.forms import BoundField
from django.template.defaultfilters import striptags

register = template.Library()
@register.simple_tag
def get_error(errors):
  #errors = token.contents
  errors = errors.__str__().split('</li>')
  for error in errors:
    return striptags(error)