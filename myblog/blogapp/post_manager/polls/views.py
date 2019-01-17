from django.shortcuts import render, redirect
from .models import Question, Choice

# Create your views here.

def vote(request, poll_id, choice_id):
	try:
		poll = Question.objects.filter(id=poll_id)[0]
		choice = Choice.objects.filter(id=choice_id)[0]
		if choice in poll.choice_set.all():
			choice.votes += 1
			choice.save()
			return redirect('blogs:home_poll', use_results=1)
		else:
			return redirect('blogs:home')
	except Exception as e:
		print(e)
		return redirect('blogs:home')
