from django.shortcuts import render
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserProfileSerializer
from users.utils import generate_unique_username
from users.models import CustomUser
from drf_yasg.utils import swagger_auto_schema
# from click_up.views import ClickWebhook
# from click_up import ClickUp


# Create your views here.

class UserAccountAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={201: UserProfileSerializer},
        operation_description="Foydalanuchi ma'lumotlari"
    )

    def get(self,request):
        serializer = UserProfileSerializer(instance = request.user)
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
    

# class ClickWebhookAPIView(ClickWebhook):
#     def successfully_payment(self, params):
#         user_id = params.get("merchant_trans_id")  
#         amount = params.get("amount")
#         try:
#             user = CustomUser.objects.get(id=user_id)
#             user.balance += float(amount)
#             user.save()
#             print(f"✅ {user.username} balansi +{amount} so‘m to‘ldirildi")
#         except CustomUser.DoesNotExist:
#             print("❌ Foydalanuvchi topilmadi")

#     def cancelled_payment(self, params):
#         print("❌ To‘lov bekor qilindi:", params)

    

# class BalanceTopUpAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         amount = request.data.get("amount")
#         if not amount:
#             return Response({"error": "Summani kiriting"}, status=400)
#         try:
#             amount = float(amount)
#             if amount <= 0:
#                 return Response({"error": "Summani to‘g‘ri kiriting"}, status=400)
#         except ValueError:
#             return Response({"error": "Summa raqam bo‘lishi kerak"}, status=400)

#         click_up = ClickUp()
#         pay_link = click_up.initializer.generate_pay_link(
#             id=request.user.id,
#             amount=amount,
#             return_url="http://174.138.69.45:8000/billing/user-account/"
#         )
#         return Response({"pay_link": pay_link})


    


