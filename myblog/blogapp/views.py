from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import BlogPost, Comment, User, AskPost, EmailSubscriber, SiteNews, Question, Choice
from django.utils import timezone
from django.views import generic
from .shared import *
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
		
def index(request):
    latest_post_list = BlogPost.objects.order_by('-pub_date')[:15]
    context = {'latest_post_list': latest_post_list}
    return render(request, 'blogapp/index.html', context)

class DetailView(HitCountDetailView):
	model = BlogPost
	count_hit = True
	template_name = 'blogapp/detail.html'
	
def about(request):
	return render(request, 'blogapp/about.html')
	
def askAaron(request):
	latest_question_list = AskPost.objects.order_by('-pub_date')
	return render(request, 'blogapp/forum/archive.html', {'question_list': latest_question_list})
	
class askAaron_detail(HitCountDetailView):
	model = AskPost
	count_hit = True
	template_name = 'blogapp/forum/detail.html'
	
def askNew(request):
	return render(request, 'blogapp/forum/askNew.html')
	
def postQuestion(request):
	if (not isValidPost(request)):
		return render(request, 'blogapp/forum/askNew.html', {'error_message': "Please fill in the required fields(*)"})
	q = AskPost(author=request.POST['username'], pub_date=timezone.now(), question_title=request.POST['questionTitle'], text=request.POST['questionBody'])
	q.save()
	emailAaron(request.POST['username'] + " just posted a new question!")
	return render(request, 'blogapp/forum/detail.html', {'askpost': q})

def archive(request):
	#TODO
	return HttpResponse("Still in development!")
	# Splits the searchString into keywords that can then be searched for relevance in all posts and questions.
	kwdarg = request.POST['searchString'].casefold().split()
	
	resultList = searchRelevantMaterial(kwdarg)
	
	return render(request, 'blogapp/index.html', {'latest_post_list': resultList})

def comment(request, article_id):
	selected_article = get_object_or_404(BlogPost, id=article_id)

	if (not isValidComment(request)):
		return render(request, 'blogapp/detail.html', {'blogpost': selected_article, 'comment_list': selected_article.comment_set, 'comment_error_message': "Please fill in the required fields"})
	
	selected_article.comment_set.create(author=request.POST['username'], pub_date=timezone.now(), text=request.POST['commentText'])
	selected_article.save()

	return render(request, 'blogapp/detail.html', {'blogpost': selected_article, 'comment_list': selected_article.comment_set})
	
def forumcomment(request, pk):
	selected_article = get_object_or_404(AskPost, pk=pk)
	
	if (not isValidComment(request)):
		return render(request, 'blogapp/forum/detail.html', {'askpost': selected_article, 'comment_list': selected_article.forumcomment_set, 'comment_error_message': "Please fill in the required fields"})
	
	selected_article.forumcomment_set.create(author=request.POST['username'], pub_date=timezone.now(), text=request.POST['commentText'])
	selected_article.save()

	return render(request, 'blogapp/forum/detail.html', {'askpost': selected_article, 'comment_list': selected_article.forumcomment_set})

def reply(request, article_id, comment_id):
    return HttpResponse("You are replying to comment %s!", comment_id)
