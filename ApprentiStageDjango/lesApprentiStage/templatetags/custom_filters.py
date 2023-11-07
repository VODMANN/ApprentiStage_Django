from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    css_classes = value.field.widget.attrs.get('class', '')
    if css_classes:
        css_classes = f"{css_classes} {arg}"
    else:
        css_classes = arg
    return value.as_widget(attrs={'class': css_classes})

@register.filter(name='add_icon')
def add_icon(field):
    icons = {
        'numEtu': 'fa-id-card',
        'nomEtu': 'fa-user',
        'prenomEtu': 'fa-user',
        'adresseEtu': 'fa-home',
        'cpEtu': 'fa-envelope',
        'villeEtu': 'fa-city',
        'telEtu': 'fa-phone',
        'promo': 'fa-graduation-cap',
        # Ajoutez d'autres mappages si nécessaire
    }
    icon_class = icons.get(field.name, 'fa-exclamation-circle')
    icon_html = f'<i class="fas {icon_class}"></i>'
    return mark_safe(icon_html)  # Marque le HTML comme sûr pour éviter l'échappement