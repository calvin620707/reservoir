from django.shortcuts import render
from django.views import View

from sheets.models import CostRecord


class ProjectReportView(View):
    def get(self, request):
        proj = request.user.current_project
        costs = CostRecord.objects.filter(project=proj).filter(calculated=False)
        return render(request, 'reports/project_report.html', {'costs': costs})

    def post(self, request):
        raise NotImplemented
