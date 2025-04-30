from django.core.exceptions import ValidationError
from PIL import Image, ImageOps
from io import BytesIO

def validate_image_aspect_ratio(image):
    """"""
    img = Image.open(image)
    width, height = img.size
    target_ratio = 4 / 3  # Соотношение 4:3
    current_ratio = width / height

    # Допустимое отклонение (например, ±5%)
    if not (0.95 * target_ratio <= current_ratio <= 1.05 * target_ratio):
        raise ValidationError("Соотношение сторон изображения должно быть 4:3.")
    
    image.seek(0)  # Сбросить указатель файла
def apply_exif_orientation(img):
    """Применяет EXIF-ориентацию к изображению и возвращает корректные размеры."""
    try:
        exif = img._getexif()
    except AttributeError:
        exif = None

    if exif is None:
        return img

    orientation = exif.get(0x0112, 1)

    if orientation == 1:
        return img
    elif orientation == 2:
        return ImageOps.mirror(img)
    elif orientation == 3:
        return img.rotate(180)
    elif orientation == 4:
        return ImageOps.flip(img)
    elif orientation == 5:
        return ImageOps.mirror(img).rotate(270)
    elif orientation == 6:
        return img.rotate(270)
    elif orientation == 7:
        return ImageOps.mirror(img).rotate(90)
    elif orientation == 8:
        return img.rotate(90)
    else:
        return img

    
def validate_ad_image(image):
    # Максимальный размер файла (5 МБ)
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Максимальный размер файла — 5 МБ.")

    # Чтение содержимого изображения
    try:
        image_content = image.read()
        image.seek(0)
    except Exception as e:
        raise ValidationError("Ошибка чтения файла.")

    # Проверка изображения и EXIF-ориентации
    try:
        img = Image.open(BytesIO(image_content))
        img = apply_exif_orientation(img)
        width, height = img.size
        img.close()
    except Exception as e:
        raise ValidationError("Недопустимый формат изображения или повреждённый файл.")

    # Проверка горизонтальной ориентации
    if width <= height:
        raise ValidationError("Изображение должно быть горизонтальной ориентации.")

    # Проверка соотношения сторон (1.91:1 ± 0.1)
    target_ratio = 1.91
    current_ratio = width / height
    ratio_tolerance = 0.1
    if not (target_ratio - ratio_tolerance <= current_ratio <= target_ratio + ratio_tolerance):
        raise ValidationError(f"Соотношение сторон должно быть ~{target_ratio}:1.")

    # Проверка минимальных размеров
    min_width, min_height = 600, 314
    if width < min_width or height < min_height:
        raise ValidationError(f"Минимальный размер: {min_width}x{min_height}px. Ваш: {width}x{height}px.")