from .models import BlogPost, EmailSubscriber
from django.db.models.query import QuerySet 
from django.core.mail import send_mail

def sqlInjectionDetect(str):
	sql_keywords = ['CREATE', 'DROP', 'ALTER', 'TRUNCATE', 'COMMENT', 'RENAME', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK', 'SAVEPOINT', 'SET TRANSACTION']
	for k in sql_keywords:
		if (str.find(k) >= 0):
			return True
	return False
	
def isValidComment(request):
	return request.POST['username'] != "" and request.POST['commentText'] != "" and not (sqlInjectionDetect(request.POST['username']) or sqlInjectionDetect(reques.POST['commentText']))
	
def isValidPost(request):
	return request.POST['username'] != "" and request.POST['questionTitle'] != "" and not (sqlInjectionDetect(request.POST['username']) or sqlInjectionDetect(request.POST['questionTitle']) or sqlInjectionDetect(request.POST['questionBody']))
	
def emailAaron(messageBody):
	send_mail(
		"Aaron's Blog Notification",
		messageBody,
		'aaronjencks@aol.com',
		['aaronjencks@aol.com'],
		fail_silently=True,
		)
		
def emailSubList(messageSubject, messageBody):
	send_mail(
		messageSubject,
		messageBody,
		'aaronjencks@aol.com',
		map(lambda x: x.email, EmailSubscriber.objects.all()),
		fail_silently=True,
		)
	
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
	