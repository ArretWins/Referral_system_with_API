from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client


from .models import User
from .serializers import UserSerializer
from .utils import generate_otp, send_otp_sms
from Referral.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

verify_sid = "VA7f6ae1a5cc074e5fcbb49f40cbd7d553"


# class UserRegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneAuthorizationView(APIView):
    def get(self, request):
        return render(request, 'main/phone_authorization.html')

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if phone_number:
            user, created = User.objects.get_or_create(phone_number=phone_number)

            if created or not user.is_verified:
                otp = generate_otp()  # Используйте вашу функцию генерации OTP
                user.otp = otp
                user.save()

                send_otp_sms(phone_number, otp)  # Отправьте SMS с кодом авторизации

                return Response({'message': 'OTP has been sent to your phone number.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User already verified.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    def get(self, request):
        return render(request, 'main/otp_verification.html')

    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        if phone_number and otp:
            try:
                user = User.objects.get(phone_number=phone_number)
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                # В этом месте нам не нужно проверять otp, потому что теперь Twilio Verify Service заботится об этом
                verification = client.verify \
                    .services(verify_sid) \
                    .verification_checks \
                    .create(to=phone_number, code=otp)
                if verification.status == 'approved':
                    user.is_verified = True
                    user.save()
                    return Response({'message': 'User has been verified successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid phone number or OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Phone number and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)
