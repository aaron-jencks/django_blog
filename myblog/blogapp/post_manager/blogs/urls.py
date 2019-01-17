from django.urls import path, include

from . import views

app_name = 'blogs'
urlpatterns = [	path('', views.index, name='index'),
		path('forum/', include('blogapp.post_manager.forum.urls')),
		path('<int:pk>/', views.DetailView.as_view(), name='detail'),
                path('<int:article_id>/comment', views.comment, name='comment'),
                path('<int:article_id>/comment/<int:comment_id>/reply', views.reply, name='reply'),
        ]
