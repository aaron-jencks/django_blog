from django.db import models
from model_utils.models import StatusModel
from hitcount.models import HitCount, HitCountMixin
from model_utils import Choices
from django.contrib.contenttypes.fields import GenericRelation
from ..models import sqlInjectionDetect

class TextPost(HitCountMixin, StatusModel):
	STATUS = Choices('published', 'draft')
	author = models.CharField(max_length=50, blank=True, null=True)
	text = models.TextField(blank=True)
	hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
	
	def __str__(self):
		return self.author + "\n" + self.pub_date.strftime(" %d/%m/%y_%H:%M")
	
	class Meta:
		abstract = True

def isValidComment(request):
	return request.POST['username'] != "" and request.POST['commentText'] != "" and not (sqlInjectionDetect(request.POST['username']) or sqlInjectionDetect(request.POST['commentText']))
	
def isValidPost(request):
	return request.POST['username'] != "" and request.POST['questionTitle'] != "" and not (sqlInjectionDetect(request.POST['username']) or sqlInjectionDetect(request.POST['questionTitle']) or sqlInjectionDetect(request.POST['questionBody']))

class PostTopic(models.Model):
	tag = models.CharField(max_length=50)
	
	def __str__(self):
		return self.tag

# Create your models here.
