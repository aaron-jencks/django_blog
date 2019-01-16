from django.urls import path

from . import views

app_name = 'blogs'
urlpatterns = [
        path('', views.home, name='home'),
		path('/<int:use_results>/', views.home, name='home_poll'),
		path('subscribe/', views.Subscribe, name='subscribe'),
		path('subscribe/Go', views.SubscribeAction, name='subscribeAction'),
		path('about/', views.about, name='about'),
		path('signup/', views.signup, name='signup'),
		path('signin/', views.signin, name="signin"),
		path('createUser/', views.createUser, name="createUser"),
		path('blog/', views.index, name='index'),
		path('blog/forum/', views.askAaron, name='askAaron'),
		path('blog/<int:pk>/', views.DetailView.as_view(), name='detail'),
		path('blog/forum/ask/new/', views.postQuestion, name='postQuestion'),
		path('blog/forum/<int:pk>/', views.askAaron_detail.as_view(), name='askAaron_detail'),
		path('blog/forum/<int:question_id>/comment', views.forumcomment, name='forumcomment'),
		path('blog/forum/ask/', views.askNew, name='askQuestion'),
        path('search/', views.archive, name='archive'),
        path('blog/<int:article_id>/comment', views.comment, name='comment'),
        path('blog/<int:article_id>/comment/<int:comment_id>/reply', views.reply, name='reply'),
		path('vote/<int:poll_id>/<int:choice_id>', views.vote, name='vote'),
        ]
