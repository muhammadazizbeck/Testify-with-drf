from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import get_user_model

from users.tasks import sent_otp_email_task
from users.models import EmailOTP
from users.serializers import RegisterSerializer,VerifyOTPSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

import random

User = get_user_model()


# Create your views here.

class RegisterAPIView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'code':201,
            'message':"Ro'yhatdan muvaffaqiyatli o'tdingiz,Emailingizga yuborilgan bir martalik parol orqali emailingizni tasdiqlang!",
            'data':serializer.data
        }

        return Response(response,status=status.HTTP_201_CREATED)
    
class VerifyOTPAPIView(APIView):
    def post(self,request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'code':"200",
            "message":"Emailingiz tasdiqlandi,Tizmga kirib foydalanishingiz mumkin!",
            "data":serializer.data
        }
        


        
class LogoutAPIView(APIView):
    def post(self,request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':"Tizimdan muvaffaqiyatli chiqildi"},status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error':"Token noto'g'ri yoki allaqachon eskirgan"},status=status.HTTP_400_BAD_REQUEST)
        
        
        



        
