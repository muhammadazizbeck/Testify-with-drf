from users.models import CustomUser
from users.utils import generate_unique_username
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

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

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Parollar bir-biriga mos kelmadi.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        username = validated_data.get('username')
        count = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{count}"
            count += 1
        validated_data['username'] = username

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.is_active = True 
        user.save()

        refresh = RefreshToken.for_user(user)
        return {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
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


