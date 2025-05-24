from django.shortcuts import render
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema


from users.models import CustomUser
from users.serializers import RegisterSerializer,\
    LoginSerializer,ChangePasswordSerializer

from rest_framework import status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

import random

User = CustomUser


# Create your views here.

class RegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer},
        operation_description="Ro'yhatdan o'tish"
    )
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()
        response = {
            'code':201,
            'message':"Ro'yhatdan muvaffaqiyatli o'tdingiz,Login sahifasi orqali tizimdan foydalanishingiz mumkin",
            'data':user_data
        }

        return Response(response,status=status.HTTP_201_CREATED)
    
class LoginAPIView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: LoginSerializer},
        operation_description="Testdagi savollar ro'yhati"
    )
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

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={200: ChangePasswordSerializer},
        operation_description="Parolni almashtirish"
    )
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
        
        
        
        
        
        

        
        
        



        
