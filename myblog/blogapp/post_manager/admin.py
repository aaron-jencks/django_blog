from django.contrib import admin
from .models import *

# Register your models here.

class TopicInline(admin.ModelAdmin):
	model = PostTopic
	extra = 3

admin.site.register(PostTopic, TopicInline)
