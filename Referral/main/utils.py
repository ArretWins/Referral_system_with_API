from twilio.rest import Client
from Referral.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
import random


def generate_otp():
    return str(random.randint(1000, 9999))


def send_otp_sms(phone_number, otp):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f'Your OTP code is: {otp}',
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    return message.sid


