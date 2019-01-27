from django.contrib import admin
from .models import *
from utils.admin import CommentInline

# Register your models here.

class TopicInline(admin.ModelAdmin):
	model = PostTopic
	extra = 3
	fk_name = 'topic'

class BlogPostAdmin(admin.ModelAdmin):
	model = BlogPost
	#inlines = [CommentInline]

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(PostTopic, TopicInline)
