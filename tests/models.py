from django.db import models
from users.models import CustomUser

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=230)

    def __str__(self):
        return self.title


class Test(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='tests')
    image = models.ImageField(upload_to='test_images/')
    title = models.CharField(max_length=120)
    description = models.TextField()
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(help_text="Test yechish davomiyligi")
    question_count = models.PositiveIntegerField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class Question(models.Model):
    test = models.ForeignKey('Test', related_name='questions', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='question_images/',blank=True,null=True)
    text = models.TextField()

    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)

    correct_option = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    

class TestResult(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    score_percentage = models.DecimalField(max_digits=5,decimal_places=2)
    coins_earned = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_first_attempt = models.BooleanField(default=False)
    

    
