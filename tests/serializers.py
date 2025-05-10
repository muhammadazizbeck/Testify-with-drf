from rest_framework import serializers
from tests.models import Category,Test,Question,UserTest
from users.serializers import CustomUserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','description']
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','text']    

class TestSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id','title','description','is_paid','price','category','duration','created_at','updated_at']

        def get_price_displey(self,obj):
            return "Bepul" if not obj.is_paid else f"{obj.price} so'm"
        
        def to_representation(self,instance):
            representation = super().to_representation(instance)
            representation['price_displey'] = self.get_price_displey(instance)
            return representation
        
class UserTestSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    test = TestSerializer()

    class Meta:
        model = UserTest
        fields = ['id', 'user', 'test', 'purchased', 'completed']


    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['purchased_status'] = "Sotib olingan" if instance.purchased else "Sotib olinmagan"
        representation['completed_status'] = "Yakunlangan" if instance.completed else "Yakunlanmagan"
        return representation
    