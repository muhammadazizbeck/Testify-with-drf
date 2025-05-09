from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import get_user_model

from users.tasks import sent_otp_email_task
from users.tokens import generate_jwt_tokens
from users.models import EmailOTP
from users.serializers import EmailSerializer,OTPVerifySerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

import random

User = get_user_model()


# Create your views here.

class SendOTPAPIView(APIView):
    def post(self,request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        otp = "".join(str(random.randint(1,9)) for _ in range(5))
        EmailOTP.objects.filter(email=email).delete()

        EmailOTP.objects.create(email=email,otp=otp)

        sent_otp_email_task.delay(email,otp)

        response = {
            'message':'Tasdiqlash uchun kodingiz emailga yuborildi'
        }

        return Response(response)
    
class VerifyOTPAPIView(APIView):
    def post(self,request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        
        try:
            otp_obj = EmailOTP.objects.get(email=email,otp=otp)

            if timezone.now()-otp_obj.created_at>timezone.timedelta(minutes=3):
                return Response({'error':'Kod muddati tugagan'},status=status.HTTP_400_BAD_REQUEST)
            
            otp_obj.is_verified = True
            otp_obj.save()

            user,created = User.objects.get_or_create(email=email)

            tokens = generate_jwt_tokens(user)

            otp_obj.delete()

            return Response({'message':"Kirish muvaffaqiyatli amaliga oshdi","tokens":tokens})
        
        except EmailOTP.DoesNotExist:
            return Response({'error':"Noto'g'ri kod yoki email"},status=status.HTTP_400_BAD_REQUEST)
        
class LogoutAPIView(APIView):
    def post(self,request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':"Tizimdan muvaffaqiyatli chiqildi"},status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error':"Token noto'g'ri yoki allaqachon eskirgan"},status=status.HTTP_400_BAD_REQUEST)
        
        
        



        
