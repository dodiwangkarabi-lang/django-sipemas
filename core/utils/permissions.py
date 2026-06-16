from core.constants import *

def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

def is_guru(user) -> bool:
    """
    mengecek apakah guru

    Args:
        user (obj): instance obeject user

    Returns:
        bool: benar jika sebagai role guru
        
    Example:
        >>> is_guru(user)
        >>> True
    """
    return has_group(user, ROLE_GURU)

def is_admin(user) -> bool:
    """
    mengecek apakah admin

    Args:
        user (obj): instance obeject user

    Returns:
        bool: benar jika sebagai role admin
        
    Example:
        >>> is_admin(user)
        >>> True
    """
    return has_group(user, ROLE_ADMIN)