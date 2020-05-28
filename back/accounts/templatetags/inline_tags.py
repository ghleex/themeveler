from django import template
register = template.Library()

@register.simple_tag
def move(request, name, page):
    copy_data = request.GET.copy()
    copy_data[name] = str(page)
    return '?' + copy_data.urlencode()
