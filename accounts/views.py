from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from accounts.models import Project


class MyProjectsView(View):
    def get(self, request):
        projects = request.user.project_set.all()
        return render(request, 'accounts/select_project.html', context={'projects': projects})


class MyNewProjectView(View):
    def get(self, request):
        return render(request, 'accounts/create_new_project.html')


class MyCurrentProjectView(CreateView):
    model = Project
    fields = ['name', 'members']
