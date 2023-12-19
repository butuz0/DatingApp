from django import template
from account.models import Interest

register = template.Library()


@register.filter
def add_attr(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, val = d.split(':')
            attrs[key] = val

    return field.as_widget(attrs=attrs)


@register.filter
def get_qs_values(queryset, key):
    qs = queryset.all().values_list(key)
    return [value[0] for value in qs]


@register.filter
def interest_to_str(value):
    val = str(value).split('>')[-2][2:-7]
    return str(val)
