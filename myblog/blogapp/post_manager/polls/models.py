from django.db import models
from model_utils.models import StatusModel
from model_utils import Choices

# Create your models here.

class Question(StatusModel):
	STATUS = Choices('published', 'draft')
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
