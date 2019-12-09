from django import template

register = template.Library()


def include_filter(value,values):
    return True if value in [int(str(x)) for x in values] else False


register.filter('include', include_filter)