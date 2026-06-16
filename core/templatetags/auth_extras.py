from django import template
from core.utils.permissions import has_group
from core.constants import *

register = template.Library()

@register.simple_tag
def role_guru():
    return ROLE_GURU

@register.simple_tag
def role_admin():
    """
    menghindari type

    Returns:
        str: nama role
        
    Example:
        {% role_admin as ROLE_ADMIN %}

        {% if request.user|user_has_group:ROLE_ADMIN %}
    """
    return ROLE_ADMIN

@register.filter
def user_has_group(user, group_name):
    """
    filter di template

    Args:
        user (obj): instance user
        group_name (str): nama group

    Returns:
       bool : kalau ada nama yang cocok maka return True
       
    Example:
        {% if user|user_has_group:"Admin" %}
    """
    return has_group(user, group_name)

