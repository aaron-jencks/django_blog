from django.db import models
from django.core.mail import send_mail
from utils.models import TextPost

# Create your models here.

class EmailBody(TextPost):
    pass

class EmailSubscriber(models.Model):
	email = models.EmailField(unique=True)

	def __str__(self):
                return self.email
	
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
