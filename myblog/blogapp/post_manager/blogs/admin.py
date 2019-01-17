from django.contrib import admin
from .models import *

# Register your models here.

class CommentInline(admin.StackedInline):
	model = Comment
	extra = 1

class BlogPostAdmin(admin.ModelAdmin):
	model = BlogPost
	inlines = [CommentInline]

admin.site.register(BlogPost, BlogPostAdmin)
