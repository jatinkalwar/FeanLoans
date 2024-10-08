import random
import string


def generate_15_digit_alpha_token():
    characters = string.ascii_letters + string.digits  # Includes uppercase, lowercase, and digits
    token = ''.join(random.choice(characters) for _ in range(15))
    return token
