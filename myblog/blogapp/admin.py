from django.contrib import admin

from .models import *

class TopicInline(admin.ModelAdmin):
	model = PostTopic
	extra = 3

class CommentInline(admin.StackedInline):
	model = Comment
	extra = 1

class BlogPostAdmin(admin.ModelAdmin):
	model = BlogPost
	inlines = [CommentInline]
	
class AnswerInline(admin.StackedInline):
	model = AskAnswer
	extra = 1
	
class AnswerCommentInline(admin.StackedInline):
	model = ForumComment
	extra = 1
	
class AskPostAdmin(admin.ModelAdmin):
	model = AskPost
	inlines = [AnswerInline, AnswerCommentInline]
	
class ChoiceInline(admin.StackedInline):
	model = Choice
	extra = 1
	
class QuestionAdmin(admin.ModelAdmin):
	model = Question
	inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(User)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(PostTopic, TopicInline)
admin.site.register(AskPost, AskPostAdmin)
admin.site.register(SiteNews)
admin.site.register(EmailSubscriber)

# Register your models here.
