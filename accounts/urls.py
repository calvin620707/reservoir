from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import MyProjectsView, MyNewProjectView, MyCurrentProjectView, MyProjectUpdateView, JoinProjectView, ProjectDetailView

app_name = 'accounts'
urlpatterns = [
    url(r'^my/projects$', login_required(MyProjectsView.as_view()), name='my-projects'),
    url(r'^my/new/project', login_required(MyNewProjectView.as_view()), name="my-new-project"),
    url(r'^my/projects/current$', login_required(MyCurrentProjectView.as_view()), name='my-current-project'),
    url(r'^my/projects/(?P<pk>[0-9]+)', login_required(MyProjectUpdateView.as_view()), name='update-my-project'),
    url(r'^join/project/(?P<project_id>[0-9]+)', login_required(JoinProjectView.as_view()), name='join-project'),
    url(r'^project/(?P<pk>[0-9]+)', login_required(ProjectDetailView.as_view()), name='project-detail')
]