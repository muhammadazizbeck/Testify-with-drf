from rest_framework import serializers
from tests.models import Test,Question


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id','title','description','is_paid','price','question_count','duration']
        extra_kwargs = {
            'id': {'help_text': 'Testning maxsus raqami'},
            'title': {'help_text': 'Testning nomi'},
            'description': {'help_text': 'Testning tavsifi'},
            'is_paid': {'help_text': 'Test pullikmi yoki bepul'},
            'price': {'help_text': 'Test narxi'},
            'question_count': {'help_text': 'Test nechta savoldan tashkil topgan'},
            'duration': {'help_text': 'Testni yechish uchun necha daqiqa beriladi'}
        }

class TestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id','title','description','is_paid','price','question_count','duration']
        extra_kwargs = {
            'id': {'help_text': 'Testning maxsus raqami'},
            'title': {'help_text': 'Testning nomi'},
            'description': {'help_text': 'Testning tavsifi'},
            'is_paid': {'help_text': 'Test pullikmi yoki bepul'},
            'price': {'help_text': 'Test narxi'},
            'question_count': {'help_text': 'Test nechta savoldan tashkil topgan'},
            'duration': {'help_text': 'Testni yechish uchun necha daqiqa beriladi'}
        }

    def validate(self,data):
        if data.get('is_paid') and not data.get('price'):
            raise serializers.ValidationError('Pulli test uchun narx kiritilishi kerak!')
        if not data.get('is_paid'):
            data['price'] = None
        return data
    

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text','option_1','option_2','option_3','option_4','correct_option']
        extra_kwargs = {
            'text': {'help_text': 'Savol'},
            'option_1': {'help_text': 'Birinchi tanlov uchun javob'},
            'option_2': {'help_text': 'Ikkinchi tanlov uchun javob'},
            'option_3': {'help_text': 'Uchinchi tanlov uchun javob'},
            'option_4': {'help_text': "To'rtinchi tanlov uchun javob"},
            'correct_option': {'help_text': "To'g'ri javobni kiriting [1,2,3,4 orasidan]"},
        }

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

class TestDetailSerializer(serializers.ModelSerializer):
    questions = QuestionCreateSerializer(many=True,read_only=True,help_text="Testga tegishli barcha savollar ro‘yxati")

    class Meta:
        model = Test
        fields = ['id','title','description','is_paid','price','question_count','duration','questions']
        extra_kwargs = {
            'id': {'help_text': 'Testning maxsus raqami'},
            'title': {'help_text': 'Testning nomi'},
            'description': {'help_text': 'Testning tavsifi'},
            'is_paid': {'help_text': 'Test pullikmi yoki bepul'},
            'price': {'help_text': 'Test narxi'},
            'question_count': {'help_text': 'Test nechta savoldan tashkil topgan'},
            'duration': {'help_text': 'Testni yechish uchun necha daqiqa beriladi'},
            'questions': {'help_text':'Barcha savollar'}
        }

    
