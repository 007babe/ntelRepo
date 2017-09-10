from django import template

register = template.Library()


@register.filter
def isMvno(objects, isMvno=True):
    return objects.filter(
        companyId__isMvno=isMvno
    )
