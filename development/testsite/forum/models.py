from django.db import models
from utils.models import TextPost, Commentable

# Create your models here.

class AskPost(TextPost, Commentable):
	question_title = models.CharField(max_length=50)
	question_answer = models.ForeignKey('AskAnswer', on_delete=models.CASCADE, blank=True, null=True)
	pass
	
class AskAnswer(TextPost):
	question_target = models.ForeignKey('AskPost', on_delete=models.CASCADE, blank=True, null=True)
	pass
