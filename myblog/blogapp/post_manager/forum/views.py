from django.shortcuts import render
from ...email_manager.models import emailAaron
from .models import AskPost

# Create your views here.

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

def forumcomment(request, pk):
	selected_article = get_object_or_404(AskPost, pk=pk)
	
	if (not isValidComment(request)):
		return render(request, 'blogapp/forum/detail.html', {'askpost': selected_article, 'comment_list': selected_article.forumcomment_set, 'comment_error_message': "Please fill in the required fields"})
	
	selected_article.forumcomment_set.create(author=request.POST['username'], pub_date=timezone.now(), text=request.POST['commentText'])
	selected_article.save()

	return render(request, 'blogapp/forum/detail.html', {'askpost': selected_article, 'comment_list': selected_article.forumcomment_set})
