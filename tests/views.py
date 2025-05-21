from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response
from tests.serializers import TestCreateSerializer

# Create your views here.

class TestCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        if not request.user.is_superuser:
            response = {
                "code":403,
                'message':'Faqatgina super-userlar test yarata oladi!'
            }
            return Response(response,status=status.HTTP_403_FORBIDDEN)
        serializer = TestCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'code':201,
                'message':'Test muvaffaqiyatli yaratildi!',
                "data":serializer.data
            }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

