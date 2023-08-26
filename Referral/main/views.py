import random
import string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client


from .models import User
from Referral.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, VERIFY_SID
from .serializers import UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_all_queryset(self):
        return super().get_queryset()


    def get_queryset(self):
        phone_number = self.request.user
        return User.objects.filter(phone_number=phone_number)

    def get(self, request):
        users = self.get_all_queryset()
        return render(request, 'main/profile.html', {'object_list': users, 'current_user': request.user})




    @action(detail=False, methods=['post'])
    def activate_invite_code(self, request):
        user = self.request.user
        invite_code = request.data.get('invite_code')

        if user.invite_code_activated:
            return Response({'detail': 'User has already activated an invite code.'}, status=400)

        if not invite_code:
            return Response({'detail': 'Invite code is required.'}, status=400)

        try:
            invite_user = User.objects.get(invite_code=invite_code)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid invite code.'}, status=400)

        user.invite_code_activated = True
        user.outher_invite_code = invite_code
        user.save()

        return Response({'detail': 'Invite code activated successfully.'}, status=200)


class PhoneAuthorizationView(APIView):
    def get(self, request):
        return render(request, 'main/phone_authorization.html')

    def post(self, request):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'message': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.verify.services(VERIFY_SID) \
            .verifications \
            .create(to=phone_number, channel="sms")

        try:
            user = User.objects.get(phone_number=phone_number)
            if not user:
                invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                user.invite_code = invite_code
                user.save()
        except User.DoesNotExist:
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
        verification = client.verify.services(VERIFY_SID) \
            .verification_checks \
            .create(to=phone_number, code=otp)

        if verification.status == 'approved':
            try:
                user = User.objects.get(phone_number=phone_number)
                login(request, user)
                token, created = Token.objects.get_or_create(user=request.user)
                data = {
                    'token': token.key,
                    'user_id': request.user.pk,
                    'phone_number': request.user.phone_number
                }
                return Response({'message': 'User logged in successfully.', "data": data}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Invalid phone number or OTP.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def get(self, request):
        return render(request, 'main/logout.html')


    def post(self, request):
        if request.user.is_authenticated:
            try:
                token = Token.objects.get(user=request.user)
                token.delete()
            except Token.DoesNotExist:
                pass

            logout(request)
            return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not logged in."}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@login_required
def DeleteProfileView(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('login')

    return render(request, 'main/delete_profile.html')