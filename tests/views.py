from django.shortcuts import render,get_object_or_404

from tests.serializers import QuestionSerializer,UserTestSerializer,TestSerializer,CategorySerializer
from tests.models import Question,UserTest,Test,Category

from users.permissions import IsSuperAdmin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions

# Create your views here.

class FreeTestAPIVIew(APIView):
    permission_classes = [permissions.AllowAny,]
    def get(self,request):
        free_tests = get_object_or_404(Test,is_paid=False)
        serializer = TestSerializer(free_tests,many=True)
        response = {
            'code':200,
            'status':'success',
            "data":serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)
    
class PaidTestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        paid_tests = get_object_or_404(Test,is_paid=True)
        serializer = TestSerializer(paid_tests,many=True)
        response = {
            'code':200,
            'status':'success',
            'data':serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)
    
class BuyPaidTestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,test_id):
        try:
            test = Test.objects.get(id=test_id,is_paid=True)
        except Test.DoesNotExist:
            response = {
                "code":204,
                'error':'Bunday test topilmadi!'
            }
            return Response(response,status=status.HTTP_204_NO_CONTENT)
        
        if UserTest.objects.filter(user=request.user,test=test,is_paid=True):
            response = {
                "message":"Siz bu testni allaqachon sotib olgansiz"
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        UserTest.objects.create(user=request.user,test=test,purchased=True)
        response = {
            'code':200,
            'message':'Siz bu testni muvaffaqiyatli sotib oldingiz'
        }
        return Response(response,status=status.HTTP_201_CREATED)

class MyTestAPIView(APIView):
    def get(self,request):
        my_tests = get_object_or_404(Test,user=request.user,purchased=True)
        tests = [test.test for test in my_tests]
        serializer = TestSerializer(tests,many=True)
        response = {
            'code':200,
            'message':"Siz sotib olgan testlar ro'yhati",
            'data':serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)
    
class CreateTestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsSuperAdmin]

    def post(self,request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'code':201,
                'message':"You have successfully created test",
                'data':serializer.data
            }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CreateCategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsSuperAdmin]

    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'code':201,
                'message':"You have successfully created category",
                "data":serializer.data
            }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    
    

    

    

