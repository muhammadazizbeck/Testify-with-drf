from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import get_user_model

from users.tasks import sent_otp_email_task
from users.models import EmailOTP,CustomUser
from users.serializers import RegisterSerializer,VerifyOTPSerializer,\
    LoginSerializer,ChangePasswordSerializer

from rest_framework import status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

import random

User = CustomUser


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
    
class LoginAPIView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = {
            'code':200,
            "message":'Siz muvaffaqiyatli tizimga kirdingiz!',
            'data':serializer.validated_data
        }

        return Response(response,status=status.HTTP_200_OK)
    
class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = {
                'code':205,
                'message':"Siz tizimdan muvaffaqiyatli chiqdingiz!"
            }
            return Response(response,status=status.HTTP_205_RESET_CONTENT)
        except:
            response = {
                'code':400,
                'message':"Nimadir xato ketdi!"
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordAPIView(APIView):
    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data,context = {"request":request})
        if serializer.is_valid():
            serializer.save()
            response = {
                'message':"Parolingiz muvaffaqiyatli o'zgartirildi"
            }
            return Response(response,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
        

        
        
        



        
