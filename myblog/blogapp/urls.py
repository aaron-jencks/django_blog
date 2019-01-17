from django.urls import path, include

from . import views

app_name = 'site'
urlpatterns = [
        path('', views.home, name='home'),
		path('/<int:use_results>/', views.home, name='home_poll'),
		path('subscribe/', views.Subscribe, name='subscribe'),
		path('subscribe/Go', views.SubscribeAction, name='subscribeAction'),
		path('about/', views.about, name='about'),
		path('signup/', views.signup, name='signup'),
		path('signin/', views.signin, name="signin"),
		path('createUser/', views.createUser, name="createUser"),
		path(r'^blog/', include('blogapp.post_manager.blogs.urls')),
                path('search/', views.archive, name='archive'),
		path(r'^vote/', include('blogapp.post_manager.polls.urls')),
        ]
