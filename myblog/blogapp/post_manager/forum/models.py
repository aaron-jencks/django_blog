from django.db import models
from .models import TextPost

# Create your models here.

class AskPost(TextPost):
	question_title = models.CharField(max_length=50)
	pass
	
class AskAnswer(TextPost):
	question_target = models.ForeignKey('AskPost', on_delete=models.CASCADE, blank=True, null=True)
	pass

class ForumComment(TextPost):
    question_target = models.ForeignKey('AskPost', on_delete=models.CASCADE, blank=True, null=True)
    comment_target = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    pass
