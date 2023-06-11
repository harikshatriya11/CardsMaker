from django import template
register = template.Library()


@register.simple_tag
def replacertag(value, char, replace_with_char):
    value = value.replace('{0}'.format(char), '{0}'.format(replace_with_char))
    return value