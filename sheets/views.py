from django.views.generic import CreateView, DetailView

from sheets.models import CostRecord


class CostDetailView(DetailView):
    model = CostRecord


class AddCostView(CreateView):
    model = CostRecord
    fields = ['name', 'cost', 'category', 'created_at', 'comment']

    def form_valid(self, form):
        form.instance.project = self.request.user.current_project
        form.instance.payer = self.request.user
        return super().form_valid(form)
