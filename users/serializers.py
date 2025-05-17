from users.models import CustomUser,EmailOTP
from users.utils import generate_unique_username
from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.utils import generate_unique_username
from users.tasks import sent_otp_email_task
from rest_framework_simplejwt.tokens import RefreshToken

User = CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email allaqachon ro‘yxatdan o‘tgan.")
        return value
    
    def validate_username(self, value):
        original_username = value
        count = 1
        while User.objects.filter(username=value).exists():
            value = f"{original_username}{count}"
            count += 1
        return value

    def validate(self,data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Parollar bir-biriga mos kelmadi")
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        base_username = validated_data.get("username")
        unique_username = generate_unique_username(base_username)
        validated_data["username"] = unique_username

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()

        otp_obj = EmailOTP.generate_otp(user.email)
        sent_otp_email_task.delay(user.email, otp_obj.otp_code)

        return user
    
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self,data):
        email = data['email']
        otp = data['otp']

        try:
            otp_obj = EmailOTP.objects.get(email=email,otp_code=otp)
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError("Noto'g'ri kod yoki email")

        if otp_obj.is_expired():
            otp_obj.delete()
            raise serializers.ValidationError("Kod eskirgan,Qayta kod olishga harakat qiling!")
        return data

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        EmailOTP.objects.filter(email=email).delete()

        refresh = RefreshToken.for_user(user)

        return {
            'user_id':user.id,
            'username':user.username,
            "email":user.email,
            'access_token':str(refresh.access_token),
            'refresh_token':str(refresh)
        }

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        email = data.get('email')
        password = data.get("password")
        try:
            user = User.objects.get(email=email) 
        except User.DoesNotExist:
            raise serializers.ValidationError('Bunday foydalanuvchi mavjud emas!')

        if not user.is_active:
            raise serializers.ValidationError("Foydalanuvchi hali tasdiqlanmagan!")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Parol noto'g'ri")
        
        refresh = RefreshToken.for_user(user)

        return {
            'username':user.username,
            'email':user.email,
            'access_token':str(refresh.access_token),
            'refresh_token':str(refresh)
        }

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self,data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Yangi parollar mos emas!")
        return data

    def validate_old_password(self,value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Eski parol noto'g'ri!")
        return value

    def save(self,*kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password1'])
        user.save()
        return user   


