import logging

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, UpdateView

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

            request.user.current_project = proj
            request.user.save()
            return HttpResponseRedirect(reverse('my-projects'))

        return render(request, 'accounts/create_new_project.html', {'form': form})

    def get(self, request):
        form = CreateNewProjectForm()
        return render(request, 'accounts/create_new_project.html', {'form': form})


class MyProjectUpdateView(UpdateView):
    model = Project
    fields = ['name', 'description', 'start_date', 'end_date', 'members']
    template_name = 'accounts/update_project.html'

    def get_success_url(self):
        return reverse('sheets-add-costs')


class MyCurrentProjectView(View):
    def post(self, request):
        """Set user's current project"""
        request.user.current_project = get_object_or_404(Project, id=request.POST['project_id'])

        return HttpResponseRedirect(reverse('sheets-add-costs'))
