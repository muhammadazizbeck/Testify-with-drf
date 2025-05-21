from rest_framework import serializers
from tests.models import Test

class TestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id','title','description','is_paid','price','question_count','duration']

    def validate(self,data):
        if data.get('is_paid') and not data.get('price'):
            raise serializers.ValidationError('Pulli test uchun narx kiritilishi kerak!')
        if not data.get('is_paid'):
            data['price'] = None
        return data
    