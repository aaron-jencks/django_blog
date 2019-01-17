from django.db import models
from django.core.mail import send_mail

# Create your models here.

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
	send_mail(
		messageSubject,
		messageBody,
		'aaronjencks@aol.com',
		map(lambda x: x.email, EmailSubscriber.objects.all()),
		fail_silently=True,
		)
