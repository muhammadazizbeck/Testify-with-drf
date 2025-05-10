from django.db import models
from users.models import CustomUser

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,related_name='tests')
    duration = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_price_display(self):
        if not self.is_paid:
            return "Bepul"
        return f"{self.price} so'm"


class Question(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE,related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text[:50]
        
class UserTest(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    purchased = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)



     
        
