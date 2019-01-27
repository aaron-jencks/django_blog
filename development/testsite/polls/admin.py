from django.contrib import admin
from .models import *

# Register your models here.

class ChoiceInline(admin.StackedInline):
	model = Choice
	extra = 1
	
class QuestionAdmin(admin.ModelAdmin):
	model = Question
	inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
