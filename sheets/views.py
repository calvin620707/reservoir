from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from sheets.models import CostRecord


class CostDetailView(DetailView):
    model = CostRecord


class CostListView(ListView):
    model = CostRecord

    def get_queryset(self):
        return CostRecord.objects.filter(
            project=self.request.user.current_project,
            payer=self.request.user
        )


class AddCostView(CreateView):
    model = CostRecord
    fields = ['name', 'cost', 'category', 'created_at', 'comment']

    def get(self, request, *args, **kwargs):
        if not request.user.current_project:
            return HttpResponseRedirect(reverse('accounts:my-projects'))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.request.user.current_project
        form.instance.payer = self.request.user
        return super().form_valid(form)


class CostUpdateView(UpdateView):
    model = CostRecord
    fields = ['payer', 'name', 'cost', 'created_at', 'comment', 'category']
