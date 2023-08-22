import random
import string

from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client


from .models import User
from Referral.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from .serializers import UserSerializer

verify_sid = "VA7f6ae1a5cc074e5fcbb49f40cbd7d553"

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PhoneAuthorizationView(APIView):
    def get(self, request):
        return render(request, 'main/phone_authorization.html')

    def post(self, request):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'message': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate 4-digit OTP
        # otp = ''.join(random.choices(string.digits, k=4))

        # Send OTP
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.verify.services(verify_sid) \
            .verifications \
            .create(to=phone_number, channel="sms")

        try:
            user = User.objects.get(phone_number=phone_number)
            # Если пользователь уже авторизован, то не меняем инвайт-код
            if not user:
                # Generate random invite code
                invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                user.invite_code = invite_code
                user.save()
        except User.DoesNotExist:
            # Generate random invite code for a new user
            invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            user = User.objects.create(phone_number=phone_number, invite_code=invite_code)

        return Response({'message': 'OTP has been sent and invite code generated.'}, status=status.HTTP_200_OK)


class PhoneLoginView(APIView):

    def get(self, request):
        return render(request, 'main/otp_login.html')

    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        if not phone_number or not otp:
            return Response({'message': 'Phone number and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        verification = client.verify.services(verify_sid) \
            .verification_checks \
            .create(to=phone_number, code=otp)

        if verification.status == 'approved':
            try:
                user = User.objects.get(phone_number=phone_number)
                login(request, user)
                return Response({'message': 'User logged in successfully.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Invalid phone number or OTP.'}, status=status.HTTP_401_UNAUTHORIZED)