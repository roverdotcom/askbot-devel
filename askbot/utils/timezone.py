from django.conf import settings
from django.utils import timezone


def get_tzinfo():
    """Return a UTC tzinfo object if USE_TZ is set, else None.

    For use in constructing datetimes for compatibility between USE_TZ=True
    and USE_TZ=False.
    """
    return timezone.utc if getattr(settings, 'USE_TZ', False) else None
