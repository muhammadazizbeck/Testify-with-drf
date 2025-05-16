from users.models import CustomUser,EmailOTP
from users.utils import generate_unique_username
from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.utils import generate_unique_username
from users.tasks import sent_otp_email_task

User = get_user_model()


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

    def validate(self,data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Parollar bir-biriga mos kelmadi")
        return data
    
    def create(self,validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        username = generate_unique_username(validated_data['username'])
        validated_data["username"]=username

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()


        otp_obj = EmailOTP.generate_otp(user.email)
        sent_otp_email_task.delay(user.email,otp_obj.otp_code)

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
        return user       


    


