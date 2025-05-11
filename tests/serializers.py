from rest_framework import serializers
from tests.models import Category,Test,Question,UserTest,Answer
from users.serializers import CustomUserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','description']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']
    
class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True) 

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']


class TestSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'is_paid', 'price', 'category', 'duration', 'created_at', 'updated_at', 'questions']

    def get_price_displey(self, obj):
        return "Bepul" if not obj.is_paid else f"{obj.price} so'm"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price_displey'] = self.get_price_displey(instance)
        return representation

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        test = Test.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers', [])
            question = Question.objects.create(test=test, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return test

        
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
    