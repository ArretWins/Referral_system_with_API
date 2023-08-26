from twilio.rest import Client
from Referral.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, VERIFY_SID
import random


def generate_otp():
    return str(random.randint(1000, 9999))


def send_otp_sms(phone_number, otp):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.verify.v2.services(VERIFY_SID) \
        .verifications \
        .create(to=phone_number, channel="sms")

    return message.sid


