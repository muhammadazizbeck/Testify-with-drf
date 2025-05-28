from django.shortcuts import render,get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response
from drf_yasg import openapi
from decimal import Decimal

from tests.serializers import TestCreateSerializer,TestSerializer,QuestionCreateSerializer,\
    TestDetailSerializer,CategorySerializer,CategoryDetailSerializer
from tests.models import Test,Category,Question,TestResult

# Create your views here.

class CategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: CategorySerializer},
        operation_description="Categoriyalar ro'yhati"
    )

    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True)
        response = {
            'code':200,
            'message':"Barcha categoriyalar",
            'data':serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)
    
class CategoryCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={201: CategorySerializer},
        operation_description="Yangi categoriya yaratish (faqat superuser)"
    )

    def post(self,request):
        if not request.user.is_superuser:
            response = {
                'code':403,
                'message':'Faqatgina super-userlar yarata oladi'
            }
            return Response(response,status=status.HTTP_403_FORBIDDEN)
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'code':201,
                'message':"Categoriya muvaffaqiyatli yaratildi",
                'data':serializer.data
            }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category_id', openapi.IN_PATH, description="Category ID", type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: CategoryDetailSerializer},
        operation_description="Categoriyaga tegishli testlar ro'yxatini olish"
    )
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            response = {
                'code': 404,
                "message": "Bunday category mavjud emas"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryDetailSerializer(category)
        response = {
            'code': 200,
            'message': 'Categoriya va unga tegishli testlar ro‘yxati',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class TestCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=TestCreateSerializer,
        responses={201: TestCreateSerializer},
        operation_description="Yangi test yaratish (faqat superuser)"
    )

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

    @swagger_auto_schema(
        responses={200: TestSerializer},
        operation_description="Tekin testlar ro'yhati"
    )

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

    @swagger_auto_schema(
        responses={200: TestSerializer},
        operation_description="Pulli testlar ro'yhati"
    )

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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'test_id', openapi.IN_PATH, description="Test ID", type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: QuestionCreateSerializer},
        operation_description="Yangi savollar yaratish"
    )

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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'test_id', openapi.IN_PATH, description="Test ID", type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: TestDetailSerializer},
        operation_description="Testdagi savollar ro'yhati"
    )
    def get(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({
                'code': 404,
                'message': "Test mavjud emas!"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = TestDetailSerializer(test)
        return Response({
            'code': 200,
            'message': "Test va uning savollari",
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    

class SubmitTestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,test_id):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            response = {
                'code':404,
                "error":"Test topilmadi"
            }
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        
        answers = request.data.get("answers",{})
        questions = test.questions.all()
        correct = 0
        total = questions.count()

        for question in questions:
            user_answer = answers.get(str(question.id))
            if user_answer and user_answer.strip()==question.correct_option.strip():
                correct += 1

        percentage = (correct / total) * 100 if total > 0 else 0
        percentage_decimal = Decimal(str(round(percentage, 2)))

        is_first_attempt = not TestResult.objects.filter(user=request.user, test=test).exists()
        coins = int(percentage) if is_first_attempt else 0

        result = TestResult.objects.create(
            user=request.user,
            test=test,
            score_percentage=percentage_decimal,
            coins_earned=coins,
            is_first_attempt=is_first_attempt
        )

        if is_first_attempt:
            request.user.coins += coins
            request.user.save()

        return Response({
            "test": test.title,
            "score_percentage": percentage_decimal,
            "coins_earned": coins,
            "is_first_attempt": is_first_attempt,
            "total_questions": total,
            "correct_answers": correct,
        }, status=201)
    

class UnlockTestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,test_id):
        user = request.user
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            response = {
                'code':404,
                'error':"Test topilmadi"
            }
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        
        if not test.is_paid:
            return Response({'message':"Bu test bepul to'lov talab qilinmaydi!"})
        
        already_taken = TestResult.objects.filter(user=user,test=test).exists()

        if already_taken:
            return Response({"message":"Bu testni oldin yechgansiz to'lov talab qilinmaydi!"})
        
        use_coins = request.data.get("use_coins",False)
        if use_coins:
            required_coins = int(test.price/Decimal(10))
            if user.coins < required_coins:
                return Response({'error':f"Yetarli coin mavjud emas!,Kerak:{required_coins} coin"},status=400)
            user.coins -= required_coins
        else:
            if user.balance < test.price:
                return Response({'error':f"Balansingiz yetarli emas!,Kerak:{test.price} so'm"},status=400)
            user.balance -= test.price
        
        user.save()
        return Response({"message":"Test muvaffaqiyatli ochildi,testga kirishingiz mumkin"})
        
        



    
    
        
