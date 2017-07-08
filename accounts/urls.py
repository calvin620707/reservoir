from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^me/projects$', login_required(views.MyProjectsView.as_view()), name='my-projects'),
    url(r'^me/new/project$', login_required(views.MyNewProjectView.as_view()), name="my-new-project"),
    url(r'^me/projects/current$', login_required(views.MyCurrentProjectView.as_view()), name='my-current-project'),
    url(r'^me/projects/(?P<pk>[0-9]+)$', login_required(views.MyProjectUpdateView.as_view()), name='update-my-project'),
    url(r'^me/projects/(?P<pk>[0-9]+)/delete$', login_required(views.MyProjectDeleteView.as_view()),
        name='delete-my-project'),
    url(r'^me/project/(?P<project_id>[0-9]+)/join$', login_required(views.JoinProjectView.as_view()),
        name='join-project'),
    url(r'^project/(?P<pk>[0-9]+)$', login_required(views.ProjectDetailView.as_view()), name='project-detail'),
    url(r'^project/memberships$', login_required(views.UpdateMembershipView.as_view()), name='update-memberships')
]
