from django.shortcuts import render
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserProfileSerializer
from users.utils import generate_unique_username
from users.models import CustomUser
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class UserAccountAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={201: UserProfileSerializer},
        operation_description="Foydalanuchi ma'lumotlari"
    )

    def get(self,request):
        serializer = UserProfileSerializer(user=request.user)
        response = {
            'code':200,
            'message':"Foydalanuvchi accounti malumotlari",
            'data':serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)
    
class UserAccountUpdataAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer},
        operation_description="Yangi test yaratish (faqat superuser)"
    )

    def put(self,request):
        data = request.data.copy()
        new_username = data.get['username']

        if new_username:
            user_model = CustomUser
            if user_model.objects.exclude(pk=request.user.pk).filter(username=new_username).exists():
                unique_username = generate_unique_username(new_username)
                data['username'] = unique_username
            
        serializer = UserProfileSerializer(request.user,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'code':200,
                'data':serializer.data
            }
            return Response(response,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


