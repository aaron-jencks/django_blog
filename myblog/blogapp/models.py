import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.db.models.query import QuerySet 
	
class SiteNews(models.Model):
	tag = models.TextField()
	pub_date = models.DateTimeField('date published', default=timezone.now())
	
	def __str__(self):
		return self.tag
		
def user_directory_path(instance, filename):
    return 'uploads/user_{0}/{1}'.format(instance.user_name, filename)

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    register_date = models.DateTimeField('date registered')
    user_name = models.CharField(max_length=50, unique=True)
    user_pass = models.CharField(max_length=200, blank=True, null=True)
    user_email = models.EmailField()
    profile_pic = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.user_name + ' @ ' + self.user_email
		
def sqlInjectionDetect(str):
	sql_keywords = ['CREATE', 'DROP', 'ALTER', 'TRUNCATE', 'COMMENT', 'RENAME', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK', 'SAVEPOINT', 'SET TRANSACTION']
	for k in sql_keywords:
		if (str.find(k) >= 0):
			return True
	return False
	
def searchRelevantMaterial(kwdargs):

	resultList = QuerySet(model=TextPost)

	for p in BlogPost.objects.all():
		title_count = 0
		body_count = 0
		author_count = 0
		
		for i in range(0,len(kwdargs) - 1):
			title_count += p.article_title.count(kwdargs[i])
			body_count += p.text.count(kwdargs[i])
			author_count += p.author.count(kwdargs[i])
			
		p.annotate(title_match_count=title_count)
		p.annotate(body_match_count=body_count)
		p.annotate(author_match_count=author_count)
		p.annotate(total_match_count=title_count + body_count + author_count)
		resultList.append(p)
	
	for p in AskPost.objects.all():
		title_count = 0
		body_count = 0
		author_count = 0
		answer_count = 0
		
		for i in range(0,len(kwdargs) - 1):
			title_count += p.question_title.count(kwdargs[i])
			body_count += p.text.count(kwdargs[i])
			author_count += p.author.count(kwdargs[i])
			for a in p.askanswer_set.all():
				answer_count += a.text.count(kwdargs[i])
			
		p.annotate(title_match_count=title_count)
		p.annotate(body_match_count=body_count)
		p.annotate(author_match_count=author_count)
		p.annotate(answer_match_count=answer_count)
		p.annotate(total_match_count=title_count + body_count + author_count + answer_count)
		resultList.append(p)
		
	resultList.order_by(total_match_count)
		
	return resultList
