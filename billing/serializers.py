from users.models import CustomUser
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','balance','coins']
        read_only_fields = ['balance','coins']
        