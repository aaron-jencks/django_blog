from django.shortcuts import render
from .models import AskPost

# Create your views here.

def index(request):

    # Retrieves all of the blog posts
    posts = AskPost.objects.all()
    
    title_list = {title.id:str(title) for title in posts}

    context = {
        'item_list': title_list,
    }

    return render(request, 'utils/index.html', context=context)
