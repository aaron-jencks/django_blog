from django.shortcuts import render
from .models import BlogPost
from hitcount.views import HitCountDetailView

# Create your views here.

def index(request):

    # Retrieves all of the blog posts
    posts = BlogPost.objects.all()
    
    title_list = {title.id:str(title) for title in posts}

    context = {
        'item_list': title_list,
    }

    return render(request, 'utils/index.html', context=context)

class DetailView(HitCountDetailView):
	model = BlogPost
	count_hit = True
	template_name = 'blog/detail.html'
    
