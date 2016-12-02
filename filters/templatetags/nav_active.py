from django.core.urlresolvers import resolve
from django.template import Library

register = Library()

@register.simple_tag
def nav_active(request, url):
    """
    In template: {% nav_active request "url_name_here" %}
    """
    url_name = resolve(request.path).url_name
    if url_name == url:
        return "active"
    return ""

# nav_active() will check the web request url_name and compare it
# to the named url group within urls.py,
# setting the active class if they match.