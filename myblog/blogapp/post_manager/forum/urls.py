from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [	path('', views.askAaron, name='askAaron'),
		path('ask/new/', views.postQuestion, name='postQuestion'),
		path('<int:pk>/', views.askAaron_detail.as_view(), name='askAaron_detail'),
		path('<int:question_id>/comment', views.forumcomment, name='forumcomment'),
		path('ask/', views.askNew, name='askQuestion'),
        ]
