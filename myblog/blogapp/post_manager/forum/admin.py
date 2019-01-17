from django.contrib import admin
from .models import *

# Register your models here.

class AnswerInline(admin.StackedInline):
	model = AskAnswer
	extra = 1
	
class AnswerCommentInline(admin.StackedInline):
	model = ForumComment
	extra = 1
	
class AskPostAdmin(admin.ModelAdmin):
	model = AskPost
	inlines = [AnswerInline, AnswerCommentInline]

admin.site.register(AskPost, AskPostAdmin)
