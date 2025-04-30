from django.core.exceptions import ValidationError
from PIL import Image

def validate_image_aspect_ratio(image):
    img = Image.open(image)
    width, height = img.size
    target_ratio = 4 / 3  # Соотношение 4:3
    current_ratio = width / height

    # Допустимое отклонение (например, ±5%)
    if not (0.95 * target_ratio <= current_ratio <= 1.05 * target_ratio):
        raise ValidationError("Соотношение сторон изображения должно быть 4:3.")
    
    image.seek(0)  # Сбросить указатель файла