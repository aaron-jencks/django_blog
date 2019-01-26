import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin
from django.utils import timezone
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import StatusModel
from ckeditor.fields import RichTextField
from django.db.models.query import QuerySet 
from django.core.mail import send_mail

class EmailSubscriber(models.Model):
	email = models.EmailField(unique=True)
	
def emailAaron(messageBody):
	send_mail(
		"Aaron's Blog Notification",
		messageBody,
		'aaronjencks@aol.com',
		['aaronjencks@aol.com'],
		fail_silently=True,
		)
		
def emailSubList(messageSubject, messageBody):
	emailAaron(messageBody)
	for sub in EmailSubscriber.objects.all():
		send_mail(
			messageSubject,
			messageBody,
			'aaronjencks@aol.com',
			[sub.email],
			fail_silently=True,
			)

class Question(models.Model):
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

class TextPost(models.Model, HitCountMixin):
	author = models.CharField(max_length=50, blank=True, null=True)
	pub_date = models.DateTimeField('date published')
	text = RichTextField()
	is_posted = models.BooleanField(default=True)
	hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
	
	def __str__(self):
		return self.author + "\n" + self.pub_date.strftime(" %d/%m/%y_%H:%M")
	
	class Meta:
		abstract = True

class BlogPost(TextPost, StatusModel):

	STATUS = Choices('draft', 'published')

	def defaultTag():
		return PostTopic.objects.get(tag="None")

	article_title = models.CharField(max_length=200)
	topic = models.ManyToManyField('PostTopic', default=[defaultTag])
	
	def __str__(self):
		return self.author + "\n" + self.pub_date.strftime(" %d/%m/%y_%H:%M") + " " + self.article_title
	
	def save(self):
	
		super(BlogPost, self).save()
		
		if self.status == BlogPost.STATUS.published:
			#Emails users that a new blog post was created
			emailSubList("Aaron's Blog: New Blog Post!", 
				"""Hello there subscriber,
				
				It is I, Aaron, from Aaron's blog, here to tell you that {} has posted a new blog post titled "{}" for everyone to see! Check it out here: {}
				
				Good day!
				
				Aaron
				""".format(self.author, self.article_title, "http://aaronjencks.net/blog/{}".format(self.id)))
		
def isValidComment(request):
	return request.POST['username'] != "" and request.POST['commentText'] != "" and not (sqlInjectionDetect(request.POST['username']) or sqlInjectionDetect(reques.POST['commentText']))

class Comment(TextPost):
    blog_target = models.ForeignKey('BlogPost', on_delete=models.CASCADE, blank=True, null=True)
    comment_target = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    pass
	
class ForumComment(TextPost):
    question_target = models.ForeignKey('AskPost', on_delete=models.CASCADE, blank=True, null=True)
    comment_target = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    pass
	
def isValidPost(request):
	return request.POST['username'] != "" and request.POST['questionTitle'] != "" and not (sqlInjectionDetect(request.POST['username']) or sqlInjectionDetect(request.POST['questionTitle']) or sqlInjectionDetect(request.POST['questionBody']))
	
class AskPost(TextPost):
	question_title = models.CharField(max_length=50)
	pass
	
class AskAnswer(TextPost):
	question_target = models.ForeignKey('AskPost', on_delete=models.CASCADE, blank=True, null=True)
	pass
	
class SiteNews(models.Model):
	tag = models.TextField()
	pub_date = models.DateTimeField('date published', default=timezone.now())
	
	def __str__(self):
		return self.tag
	
class PostTopic(models.Model):
	tag = models.CharField(max_length=50)
	
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
