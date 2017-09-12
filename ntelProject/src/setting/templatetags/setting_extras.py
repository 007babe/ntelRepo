from django import template

register = template.Library()


@register.filter
def mvnoYn(objects, mvnoYn=True):
    return objects.filter(
        companyId__mvnoYn__exact=mvnoYn
    )


@register.filter
def lineTpCabled(objects):
    return objects.filter(
        companyId__lineTp__srtCd__in=["A", "C"]
    )
