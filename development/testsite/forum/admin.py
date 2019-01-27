from django.contrib import admin
from .models import *
from utils.admin import CommentInline

# Register your models here.

##class AnswerInline(admin.StackedInline):
##	model = AskAnswer
##	extra = 1
##	fk_name = 'question_target'

class AskPostAdmin(admin.ModelAdmin):
	model = AskPost
	#inlines = [AnswerInline]

admin.site.register(AskPost, AskPostAdmin)
