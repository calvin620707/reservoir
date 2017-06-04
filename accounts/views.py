import logging
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView

from accounts.models import Project

logger = logging.getLogger()


class MyProjectsView(ListView):
    model = Project
    template_name = 'accounts/select_project.html'


class CreateNewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(cleaned_data)
        e_date = cleaned_data.get('end_date')
        s_date = cleaned_data.get('start_date')
        if (e_date and s_date) and (e_date < s_date):
            raise forms.ValidationError("End date should be greater than start date.")


class MyNewProjectView(View):
    def post(self, request):
        form = CreateNewProjectForm(request.POST)
        if form.is_valid():
            proj = Project(name=form.cleaned_data['name'])
            proj.save()
            proj.members.add(request.user)
            proj.save()
            return HttpResponseRedirect(reverse('my-projects'))

        return render(request, 'accounts/create_new_project.html', {'form': form})

    def get(self, request):
        form = CreateNewProjectForm()
        return render(request, 'accounts/create_new_project.html', {'form': form})


class MyCurrentProjectView(CreateView):
    model = Project
    fields = ['name', 'members']
    template_name = 'accounts/create_new_project.html'
