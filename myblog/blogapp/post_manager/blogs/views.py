from django.shortcuts import render
from .models import BlogPost, Comment
from hitcount.views import HitCountDetailView

# Create your views here.

def index(request):
    latest_post_list = BlogPost.objects.order_by('-pub_date')[:15]
    context = {'latest_post_list': latest_post_list}
    return render(request, 'blogapp/index.html', context)

class DetailView(HitCountDetailView):
	model = BlogPost
	count_hit = True
	template_name = 'blogapp/detail.html'

def comment(request, article_id):
	selected_article = get_object_or_404(BlogPost, id=article_id)

	if (not isValidComment(request)):
		return render(request, 'blogapp/detail.html', {'blogpost': selected_article, 'comment_list': selected_article.comment_set, 'comment_error_message': "Please fill in the required fields"})
	
	selected_article.comment_set.create(author=request.POST['username'], pub_date=timezone.now(), text=request.POST['commentText'])
	selected_article.save()

	return render(request, 'blogapp/detail.html', {'blogpost': selected_article, 'comment_list': selected_article.comment_set})

def reply(request, article_id, comment_id):
    return HttpResponse("You are replying to comment %s!", comment_id)
