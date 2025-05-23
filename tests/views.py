from django.shortcuts import render,get_object_or_404

from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response

from tests.serializers import TestCreateSerializer,TestSerializer,QuestionCreateSerializer,\
    TestDetailSerializer
from tests.models import Test

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

class FreeTestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        tests = Test.objects.filter(is_paid=False)
        serializer = TestSerializer(tests,many=True)
        response = {
            'code':200,
            'message':"Tekin testlar ro'yhatini oldingiz!",
            "data":serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)
    
class PaidTestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        tests = Test.objects.filter(is_paid=True)
        serializer = TestSerializer(tests,many=True)
        response = {
            'code':200,
            'message':"Pulli testlar ro'yhatini oldingiz!",
            'data':serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)
    

class QuestionCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, test_id):
        if not request.user.is_superuser:
            return Response(
                {'code': 403, 'message': "Faqat superuser savol qo‘shishi mumkin"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response(
                {'code': 400, 'message': "Test topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = QuestionCreateSerializer(data=request.data, context={'test': test})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 201,
                'message': "Savol muvaffaqiyatli qo'shildi",
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class TestDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,test_id):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            response = {
                'code':404,
                'message':"Test mavjud emas!",
            }
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        serializer = TestDetailSerializer(test)
        response = {
            'code':200,
            'message':"Testlar ro'yhati",
            'data':serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)
    
        
