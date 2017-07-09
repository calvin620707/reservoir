from collections import namedtuple, defaultdict

from django.shortcuts import render
from django.views import View

from sheets.models import CostRecord


class ReportResult:
    sum = 0
    avt = 0.0
    user_reports = {}


class ProjectReportView(View):
    def get(self, request):
        proj = request.user.current_project
        costs = CostRecord.objects.filter(project=proj).filter(calculated=False)
        result = ReportResult()

        for user in proj.members.all():
            result.user_reports[user] = {'paid': 0, 'result': {'should_get': True, 'value': 0}}

        for cost in costs:
            result.sum += cost.cost
            result.user_reports[cost.payer]['paid'] += cost.cost

        result.avg = round(result.sum / proj.members.count())

        for user in result.user_reports:
            diff = result.avg - result.user_reports[user]['paid']
            result.user_reports[user]['result']['should_get'] = diff > 0
            result.user_reports[user]['result']['value'] = abs(diff)

        return render(request, 'reports/project_report.html', {'costs': costs, 'result': result})

    def post(self, request):
        raise NotImplemented
