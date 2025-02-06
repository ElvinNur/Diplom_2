import random
import string

def generate_unique_user():
    """Генерирует уникальные данные пользователя."""
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return {
        "email": f"user_{random_part}@example.com",
        "password": "securepassword",
        "name": f"User{random_part}"
    }
