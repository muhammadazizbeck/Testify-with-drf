from rest_framework import serializers
from tests.models import Test,Question,Category,TestResult

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id",'title']

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id',"category","image",'title','description','is_paid','price','question_count','duration']

class CategoryDetailSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True,read_only=True)
    
    class Meta:
        model = Category
        fields = ["id",'title','tests']

class TestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id',"category","image",'title','description','is_paid','price','question_count','duration']

    def validate(self,data):
        if data.get('is_paid') and not data.get('price'):
            raise serializers.ValidationError('Pulli test uchun narx kiritilishi kerak!')
        if not data.get('is_paid'):
            data['price'] = None
        return data
    

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text',"image",'option_1','option_2','option_3','option_4','correct_option']

    def validate(self,data):
        correct_option = data.get('correct_option')
        if correct_option not in [1,2,3,4]:
            raise serializers.ValidationError("Correct_option 1 dan 4 gacha bo'lishi kerak")
        return data
    
    def create(self, validated_data):
        test = self.context['test']

        if test.questions.count() >= test.question_count:
            raise serializers.ValidationError("Test uchun maksimal savollar soni {test.question_count}")
        return Question.objects.create(test=test,**validated_data)
    

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'text', 'image',
            'option_1', 'option_2', 'option_3', 'option_4',
        ]

class TestDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True,read_only=True)

    class Meta:
        model = Test
        fields = ['id',"image",'title','description','is_paid','price','question_count','duration','questions']

    
class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id', 'test', 'score_percentage', 'coins_earned', 'created_at']




    
