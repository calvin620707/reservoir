from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView

from accounts.models import Project


class MyProjectsView(ListView):
    model = Project
    template_name = 'accounts/select_project.html'


class MyNewProjectView(View):
    def get(self, request):
        return render(request, 'accounts/create_new_project.html')


class MyCurrentProjectView(CreateView):
    model = Project
    fields = ['name', 'members']
