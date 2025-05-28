from django.contrib import admin
from tests.models import Category,Test,Question,TestResult

# Register your models here.

admin.site.register(Category)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(TestResult)