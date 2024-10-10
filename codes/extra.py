import random
import string
from datetime import datetime

import pytz
import requests


def application_token_gen():
    return ''.join([str(random.randint(0, 9)) for _ in range(15)])


def transaction_token():
    return ''.join([str(random.randint(0, 9)) for _ in range(20)])


def generate_15_digit_alpha_token():
    characters = string.ascii_letters + string.digits  # Includes uppercase, lowercase, and digits
    token = ''.join(random.choice(characters) for _ in range(15))
    return token

def get_time():
    # Get the current time in the IST timezone
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    # Format the date and time
    return now.strftime("%d %B %Y %I:%M %p")

async def getotp(num , otp):
    try:
        response = requests.get(f"https://otp.skotpcenter.shop/dev/api?authorization=9HKXU0hcY4NAq7x3SubRgiMGyw9tEzTZuomakDb5PL2nO1e6jf1wS8QXm2kAUtWgc0drLBElzsK7xYuh&route=dlt&sender_id=KMLETP&message=404&variables_values={otp}%7C&flash=0&numbers={num}")
        body = response.json()
        if body['return'] is True:
            return "ok"
        else:
            return "fail"
    except Exception as e:
        print(e)
        return "fail"

def generate_otp():
    otp = random.randint(100000, 999999)
    return otp
