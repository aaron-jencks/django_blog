from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin
from ckeditor.fields import RichTextField
from polymorphic.models import PolymorphicModel

class TextPost(models.Model, HitCountMixin):
	author = models.CharField(max_length=50, blank=True, null=True)
	pub_date = models.DateTimeField('date published')
	text = RichTextField()
	is_posted = models.BooleanField(default=True)
	hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
	
	def __str__(self):
		return self.author + "\n" + self.pub_date.strftime(" %d/%m/%y_%H:%M")

class Comment(TextPost):
    pass

class Commentable():
        comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comments')

def isValidComment(request):
	return request.POST['username'] != "" and request.POST['commentText'] != "" and not (sqlInjectionDetect(request.POST['username']) or sqlInjectionDetect(reques.POST['commentText']))

def sqlInjectionDetect(str):
	sql_keywords = ['CREATE', 'DROP', 'ALTER', 'TRUNCATE', 'COMMENT', 'RENAME', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK', 'SAVEPOINT', 'SET TRANSACTION']
	for k in sql_keywords:
		if (str.find(k) >= 0):
			return True
	return False
