"""reservoir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import MyProjectsView, MyCurrentProjectView, MyNewProjectView, MyProjectUpdateView
from sheets import views as sheets_views

urlpatterns = [
    url(r'^$', sheets_views.add_costs, name='sheets-add-costs'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^my/projects$', login_required(MyProjectsView.as_view()), name='my-projects'),
    url(r'^my/new/project', login_required(MyNewProjectView.as_view()), name="my-new-project"),
    url(r'^my/projects/current$', login_required(MyCurrentProjectView.as_view()), name='my-current-project'),
    url(r'^my/projects/(?P<pk>[0-9]+)', login_required(MyProjectUpdateView.as_view()), name='update-my-project'),
    url(r'^admin/', admin.site.urls)
]
