import os
import random
import string

from src.core.config import settings


def get_available_name(filename: str):
    name, extension = os.path.splitext(filename)
    while os.path.exists(settings.MEDIA_ROOT + filename):
        filename = '%s_%s%s' % (name, get_random_string(5), extension)
    return filename


def get_random_string(length=5, allowed_chars=None):
    if allowed_chars is None:
        allowed_chars = string.ascii_letters
    return ''.join(random.choice(allowed_chars) for _ in range(length))
