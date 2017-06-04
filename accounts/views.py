from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView

from accounts.models import Project


class MyProjectsView(ListView):
    model = Project
    template_name = 'accounts/select_project.html'


class CreateNewProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name']


class MyNewProjectView(View):
    def post(self, request):
        form = CreateNewProjectForm(request.POST)
        if form.is_valid():
            proj = Project(name=form.cleaned_data['name'])
            proj.save()
            proj.members.add(request.user)
            proj.save()
            return HttpResponseRedirect(reverse('my-projects'))

    def get(self, request):
        form = CreateNewProjectForm()
        return render(request, 'accounts/create_new_project.html', {'form': form})


class MyCurrentProjectView(CreateView):
    model = Project
    fields = ['name', 'members']
    template_name = 'accounts/create_new_project.html'
