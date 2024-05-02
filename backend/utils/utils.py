import re
from io import BytesIO

from PIL import Image as PilImage
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_redis import get_redis_connection


def clear_cache(patterns):
    """Clear Redis cache by create or updating objects."""

    cache_name = 'default'
    if settings.CACHES[cache_name]['BACKEND'] == 'django_redis.cache.RedisCache':
        redis_conn = get_redis_connection(cache_name)
        for pattern in patterns:
            keys = redis_conn.keys(pattern)
            if keys:
                redis_conn.delete(*keys)


def generate_redis_key(self, prefix):
    """Generate key for redis cache"""

    user_id = 'anonymous'

    return f'{prefix}:{user_id}'


def to_translit(text):
    """Translator cyrillic letters into Latin."""

    translit_dict = {
        u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g', u'д': 'd',
        u'е': 'e', u'ё': 'yo', u'ж': 'zh', u'з': 'z', u'и': 'i',
        u'й': 'y', u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n',
        u'о': 'o', u'п': 'p', u'р': 'r', u'с': 's', u'т': 't',
        u'у': 'u', u'ф': 'f', u'х': 'h', u'ц': 'c', u'ч': 'ch',
        u'ш': 'sh', u'щ': 'shch', u'ъ': '', u'ы': 'y', u'ь': '',
        u'э': 'e', u'ю': 'yu', u'я': 'ya', u'j': 'j', u'q': 'q',
        u'w': 'w', u'x': 'x', u'0': '0', u'1': '1', u'2': '2',
        u'3': '3', u'4': '4', u'5': '5', u'6': '6', u'7': '7',
        u'8': '8', u'9': '9', u' ': '-'
    }

    translit_text = [translit_dict.get(c, c) for c in text.lower()]
    for item in translit_text:
        if item not in translit_dict.values():
            translit_text[translit_text.index(item)] = '-'
    translit_text = ''.join(translit_text)
    slug = re.sub(r'[-]+', '-', translit_text.replace(' ', '-'))
    cut_slug = slug[:settings.NAME]
    return cut_slug


def reduce_image(img, max_size, image_name):
    """Reduce image to different sizes with minimum size requirement."""

    width, height = img.size
    if width < max_size and height < max_size:
        max_dim = max(width, height)
        if max_dim < max_size:
            ratio = max_size / max_dim
            new_width = int((float(width) * float(ratio)))
            new_height = int((float(height) * float(ratio)))
            img = img.resize((new_width, new_height), PilImage.LANCZOS)
    else:
        if width > height:
            ratio = max_size / float(width)
            new_height = int((float(height) * float(ratio)))
            img = img.resize((max_size, new_height), PilImage.LANCZOS)
        else:
            ratio = max_size / float(height)
            new_width = int((float(width) * float(ratio)))
            img = img.resize((new_width, max_size), PilImage.LANCZOS)
    output = BytesIO()
    img.save(
        output, format='JPEG', quality=settings.PHOTO_QUALITY,
        method=settings.PHOTO_RATIO
    )
    output.seek(0)
    return InMemoryUploadedFile(
        output, 'ImageField', f'{image_name}_{max_size}.jpg',
        'image/jpg', output.getbuffer().nbytes, None
    )


def normalize_phone(phone):
    """
    Normalize a given phone number to a standard format.
    Parameters:
        phone (str): The phone number to be normalized.
    Returns:
        str or None: The normalized phone number if it matches the expected
        pattern, otherwise returns None.
    """

    numbers_only = re.sub(r'\D', '', phone)
    pattern = r'^(\+?7|8)(\d{3})(\d{3})(\d{2})(\d{2})$'
    match = re.match(pattern, numbers_only)

    if match:
        groups = match.groups()
        normalized = f"+7 ({groups[1]}) {groups[2]}-{groups[3]}-{groups[4]}"
        return normalized
    else:
        return None
