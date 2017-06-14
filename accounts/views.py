import logging

from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DetailView, DeleteView

from accounts.models import Project

logger = logging.getLogger()


class MyProjectsView(ListView):
    model = Project

    def get_queryset(self):
        return self.request.user.project_set.all()


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
            return HttpResponseRedirect(reverse('accounts:project-detail', kwargs={'pk': proj.id}))

        return render(request, 'accounts/create_new_project.html', {'form': form})

    def get(self, request):
        form = CreateNewProjectForm()
        return render(request, 'accounts/create_new_project.html', {'form': form})


class MyProjectUpdateView(UpdateView):
    model = Project
    fields = ['name', 'description', 'start_date', 'end_date', 'members']
    template_name = 'accounts/update_project.html'

    def get_success_url(self):
        return reverse('sheets:add-costs')


class MyProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('accounts:my-projects')


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['invite_link'] = self.request.build_absolute_uri(
            reverse('accounts:join-project', kwargs={'project_id': context['object'].id})
        )
        return context


class MyCurrentProjectView(View):
    def post(self, request):
        """Set user's current project"""
        request.user.current_project = get_object_or_404(Project, id=request.POST['project_id'])
        request.user.save()

        return HttpResponseRedirect(reverse('sheets:add-costs'))


class JoinProjectView(View):
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        return render(request, 'accounts/join_project.html', context={'project': project})

    def post(self, request, project_id):
        """Join a let current user join given project"""
        project = get_object_or_404(Project, id=project_id)
        project.members.add(request.user)
        request.user.current_project = project

        project.save()
        request.user.save()

        return HttpResponse("You joined {}".format(project.name))
