from django import template

register = template.Library()


@register.filter
def index(sequence, position):
    return sequence[position]


@register.filter
def last_index(sequence):
    return sequence[len(sequence) - 1]
