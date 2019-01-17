from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
		path('<int:poll_id>/<int:choice_id>', views.vote, name='vote'),
        ]
