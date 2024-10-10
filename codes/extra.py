import random
import string
from datetime import datetime
def application_token_gen():
    return ''.join([str(random.randint(0, 9)) for _ in range(15)])


def transaction_token():
    return ''.join([str(random.randint(0, 9)) for _ in range(20)])


def generate_15_digit_alpha_token():
    characters = string.ascii_letters + string.digits  # Includes uppercase, lowercase, and digits
    token = ''.join(random.choice(characters) for _ in range(15))
    return token

def get_time():
    now = datetime.now()

    # Format the date and time
    return now.strftime("%d %B %Y %I:%M%p")
