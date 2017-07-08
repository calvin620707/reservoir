import logging

from django.http import HttpResponseRedirect, HttpResponse, request
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.views.generic.base import ContextMixin

from accounts.forms import CreateNewProjectForm, UpdateProjectForm, MembershipFormSet
from accounts.models import Project, ProjectMembership
from accounts.util import refresh_project_memberships

logger = logging.getLogger()


class MyProjectsView(ListView):
    model = Project

    def get_queryset(self):
        return self.request.user.project_set.all()


class MyNewProjectView(View):
    def post(self, request):
        form = CreateNewProjectForm(request.POST)
        if form.is_valid():
            proj = Project.objects.create(name=form.cleaned_data['name'])

            refresh_project_memberships(proj, [request.user])

            request.user.current_project = proj
            request.user.save()
            return HttpResponseRedirect(reverse('accounts:project-detail', kwargs={'pk': proj.id}))

        return render(request, 'accounts/create_new_project.html', {'form': form})

    def get(self, request):
        form = CreateNewProjectForm()
        return render(request, 'accounts/create_new_project.html', {'form': form})


class MyProjectUpdateView(UpdateView, ContextMixin):
    model = Project
    form_class = UpdateProjectForm
    template_name = 'accounts/update_project.html'

    def get_success_url(self):
        return reverse('accounts:update-my-project', kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['invite_link'] = self.request.build_absolute_uri(
            reverse('accounts:join-project', kwargs={'project_id': context['object'].id})
        )

        context['membership_formset'] = MembershipFormSet(
            queryset=ProjectMembership.objects.filter(project=context['object'])
        )
        return context


class UpdateMembershipView(View):
    def post(self, request):
        formset = MembershipFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('sheets:add-costs'))
        return render(request, 'accounts/update_project.html', {'membership_formset': formset})


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
        members = list(project.members.all())
        members.append(request.user)
        refresh_project_memberships(project, members)
        request.user.current_project = project
        request.user.save()

        return HttpResponse("You joined {}".format(project.name))
