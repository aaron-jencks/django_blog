from django.shortcuts import render
from hitcount.views import HitCountDetailView

# Create your views here.

class DetailView(HitCountDetailView):
	model = BlogPost
	count_hit = True
	template_name = 'blogapp/detail.html'

def index(request):
    latest_post_list = BlogPost.objects.order_by('-pub_date')[:15]
    context = {'latest_post_list': latest_post_list}
    return render(request, 'blogapp/index.html', context)
