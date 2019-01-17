from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .post_manager.blogs.models import BlogPost
from .post_manager.forum.models import AskPost
from .post_manager.polls.models import Question, Choice
from .email_manager.models import EmailSubscriber
from .models import User, SiteNews
from django.utils import timezone
from django.views import generic
from hitcount.views import HitCountDetailView
from django.core.validators import validate_email

def home(request, use_results=0):
	latest_post_list = BlogPost.objects.order_by('-pub_date')[:5]
	latest_question_list = AskPost.objects.order_by('-pub_date')[:5]
	latest_news_list = SiteNews.objects.order_by('-pub_date')[:5]
	context = {'latestblog_activity_list': latest_post_list, 'latestquestion_activity_list': latest_question_list, 'latestnews_activity_list': latest_news_list, 'selected_poll': Question.objects.order_by('-pub_date')[0]}
	if use_results == 1:
		# Displays the poll results to the page
		context['show_poll_result'] = True
	return render(request, 'blogapp/home.html', context)
		

def signup(request):
	return render(request, 'blogapp/signup.html')
	
def createUser(request):
	if(User.objects.filter(user_name__exact=request.POST.get('username')).count() != 0):
		return render(request, 'blogapp/signup.html', {'error_message': "That user already exists!"})
	else:
		if(request.POST.get('username').isalnum() and (str(request.POST['password']) == str(request.POST['confirmPass']))):
			newUser = User(register_date=timezone.now(), user_name=request.POST['username'], user_email=request.POST['email'], user_pass=request.POST['password'])
			newUser.save()
			return render(request, 'blogapp/home.html', {'current_user': newUser})
		else:
			return render(request, 'blogapp/signup.html', {'error_message': "Username is invalid, or passwords don't match"})
	
def signin(request):
	try:
		selected_user = User.objects.get(user_name=request.POST['username'])
		if(selected_user.user_pass == request.POST['password']):
			return render(request, 'blogapp/home.html', {'current_user': selected_user})
		else:
			return render(request, 'blogapp/home.html', {'error_message': "Incorrect username or password!"})
	except (KeyError, User.DoesNotExist):
		return render(request, 'blogapp/home.html', {'error_message': "Incorrect username or password!"})

def Subscribe(request):
	return render(request, 'blogapp/subscribeForm.html')
	
def SubscribeAction(request):
	if (not sqlInjectionDetect(request.POST['email']) and validate_email(request.POST['email'])):
		try:
			s = EmailSubscriber(email=request.POST['email'])
			s.save()
			return render(request, 'blogapp/SubscribeSuccess.html')
		except:
			return render(request, 'blogapp/subscribeForm.html', {'error_message': "That email address is invalid or already taken"})
	else:
		return render(request, 'blogapp/subscribeForm.html', {'error_message': "That email address is invalid"})
	
def about(request):
	return render(request, 'blogapp/about.html')

def archive(request):
	#TODO
	return HttpResponse("Still in development!")
	# Splits the searchString into keywords that can then be searched for relevance in all posts and questions.
	kwdarg = request.POST['searchString'].casefold().split()
	
	resultList = searchRelevantMaterial(kwdarg)
	
	return render(request, 'blogapp/index.html', {'latest_post_list': resultList})
