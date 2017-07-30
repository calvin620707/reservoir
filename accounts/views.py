import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView

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


def update_project_view(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    invite_link = request.build_absolute_uri(
        reverse('accounts:join-project', kwargs={'project_id': proj.id})
    )
    if request.method == 'POST':
        project_form = UpdateProjectForm(request.POST, instance=proj, prefix='project')
        memberships_formset = MembershipFormSet(request.POST, prefix='memberships')
        if all([project_form.is_valid(), memberships_formset.is_valid()]):
            project_form.save()
            memberships_formset.save()
    else:
        project_form = UpdateProjectForm(instance=proj, prefix='project')
        memberships_formset = MembershipFormSet(
            queryset=ProjectMembership.objects.filter(project=proj),
            prefix='memberships'
        )

    return render(request, 'accounts/update_project.html', {
        'project_form': project_form,
        'memberships_formset': memberships_formset,
        'invite_link': invite_link,
        'is_updated': True if request.method == 'POST' else False
    })


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

        messages.add_message(request, messages.SUCCESS, "You joined {}.".format(project.name))

        return HttpResponseRedirect(reverse('sheets:add-costs'))
