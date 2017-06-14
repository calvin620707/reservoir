from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^my/projects$', login_required(views.MyProjectsView.as_view()), name='my-projects'),
    url(r'^my/new/project$', login_required(views.MyNewProjectView.as_view()), name="my-new-project"),
    url(r'^my/projects/current$', login_required(views.MyCurrentProjectView.as_view()), name='my-current-project'),
    url(r'^my/projects/(?P<pk>[0-9]+)$', login_required(views.MyProjectUpdateView.as_view()), name='update-my-project'),
    url(r'^my/projects/(?P<pk>[0-9]+)/delete$', login_required(views.MyProjectDeleteView.as_view()),
        name='delete-my-project'),
    url(r'^my/project/(?P<project_id>[0-9]+)/join$', login_required(views.JoinProjectView.as_view()),
        name='join-project'),
    url(r'^project/(?P<pk>[0-9]+)$', login_required(views.ProjectDetailView.as_view()), name='project-detail')
]
