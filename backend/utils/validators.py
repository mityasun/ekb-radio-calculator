import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import FileExtensionValidator
from rest_framework import serializers


def validate_value(
        value, name_1, name_2, regex_1, regex_2, min_length, max_length
):
    """Validator for values."""

    pattern = re.compile(regex_1)

    if pattern.fullmatch(value) is None:
        symbols = re.findall(regex_2, value)
        invalid_symbols = ', '.join(symbols)
        raise ValidationError(
            f'Некорректные символы в {name_1}: {invalid_symbols}'
        )
    elif len(value) < min_length or len(value) > max_length:
        raise ValidationError(
            f'Длина {name_2} должна быть от {min_length} до {max_length} '
            f'символов.'
        )
    return value


def validate_text(name, max_length):
    """Validator for text."""

    validate_value(
        name, 'тексте', 'названия',
        r'^[A-Za-zА-ЯЁа-яё\d№&,!?."+ -:—|©@<>«»;:–\n\s]+$',
        r'[^[A-Za-zА-ЯЁа-яё\d№&,!?."+ -:—|©@<>«»;:–\n\s]',
        settings.MIN_LENGTH, max_length
    )


def validate_user_first_or_last_name(name):
    """Validator for user firstname and lastname"""

    validate_value(
        name, 'имени или фамилии', 'имени или фамилии',
        r'^[A-Za-zА-ЯЁа-яё -]+$', r'[^A-Za-zА-ЯЁа-яё -]',
        settings.MIN_LENGTH, settings.FIRST_NAME
    )


def validate_username(username):
    """Validate username"""

    validate_value(
        username, 'никнейме', 'никнейма', r'^[A-Za-z-\d]+$', r'[^A-Za-z-\d]',
        settings.MIN_USERNAME, settings.USERNAME
    )


def validate_email(email):
    """Validator for email"""

    validate_value(
        email, 'email', 'email', r'^[A-Za-z-.@\d_]+$', r'[^A-Za-z-.@\d_]',
        settings.MIN_EMAIL, settings.EMAIL
    )


def validate_phone(phone):
    """Validator for phone"""

    validate_value(
        phone, 'телефоне', 'телефона', r'^[-\d+() ]+$', r'[^-\d+() ]',
        settings.MIN_PHONE, settings.PHONE
    )


def validate_password(password):
    """Validate password"""

    if len(password) < settings.MIN_PASSWORD or len(
            password) > settings.PASSWORD:
        raise ValidationError(
            f'Длина пароля должна быть от {settings.MIN_PASSWORD} до '
            f'{settings.PASSWORD} символов.'
        )

    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!?@#$%^&*"\'|(){}\]\[<>:\/;\\.,_~+=-])[A-Za-z\d!?@#$%^&*"\'|(){}\]\[<>:\/;\\.,_~+=-]+$'

    symbols = []

    if not re.match(regex, password):
        for symbol in password:
            if not re.match(
                    r'[A-Za-z\d!?@#$%^&*"\'|(){}\]\[<>:\/;\\.,_~+=-]', symbol
            ):
                symbols.append(symbol)
        invalid_symbols = ', '.join(symbols)
        raise ValidationError(
            'Пароль должен содержать хотя бы 1 заглавную букву, 1 прописную '
            'букву, 1 цифру, 1 спецсимвол. '
            f'Некорректные символы: {invalid_symbols}'
        )
    return password


def get_available_image_extensions():
    try:
        from PIL import Image
    except ImportError:
        return []
    else:
        Image.init()
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
        return allowed_extensions


def validate_image_file_extension(value):
    allowed_extensions = get_available_image_extensions()
    return FileExtensionValidator(allowed_extensions=allowed_extensions)(value)


def validate_image(image):
    """Validate images"""

    validate_image_file_extension(image)
    width, height = get_image_dimensions(image)
    if image.size > settings.MAX_IMAGE_SIZE:
        raise ValidationError('Максимальный размер файла - 1мб.')
    if width > settings.MAX_IMAGE_RESOLUTION or (
            height > settings.MAX_IMAGE_RESOLUTION
    ):
        raise ValidationError(
            f'Размеры изображения не должны превышать '
            f'{settings.MAX_IMAGE_RESOLUTION} пикселей по одной из сторон.'
        )
    if width < settings.MIN_IMAGE_RESOLUTION or (
            height < settings.MIN_IMAGE_RESOLUTION
    ):
        raise ValidationError(
            f'Размеры изображения должны быть не меньше  '
            f'{settings.MIN_IMAGE_RESOLUTION} пикселей по одной из сторон.'
        )
    max_ratio = 16 / 9
    aspect_ratio = width / height
    if aspect_ratio > max_ratio or aspect_ratio < 1 / max_ratio:
        raise ValidationError(
            'Соотношение сторон изображения должно быть не меньше 16:9'
        )
    return image


def validate_search_query(query):
    """Validate search query."""

    if query == "" or query.isspace():
        raise serializers.ValidationError({'error': 'Пустой запрос на поиск'})
    validate_value(
        query, 'поисковом запросе', 'поискового запроса',
        r'^[A-Za-zА-ЯЁа-яё\d№&,!?."+ -:—|]+$',
        r'[^[A-Za-zА-ЯЁа-яё\d№&,!?."+ -:—|]',
        settings.MIN_LENGTH, settings.MAX_SEARCH
    )
    return query


def validate_excel_file(value):
    """Validate excel file extension."""

    allowed_extensions = ['xls', 'xlsx']
    return FileExtensionValidator(allowed_extensions=allowed_extensions)(value)
