from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name= 'reports'
urlpatterns = [
    url(r'^me/projects/current$', login_required(views.ProjectReportView.as_view()), name='current-project-report')
]