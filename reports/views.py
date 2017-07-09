from collections import namedtuple, defaultdict

from django.shortcuts import render, get_object_or_404
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

        result.avg = result.sum / proj.members.count()

        for user in result.user_reports:
            diff = result.avg - result.user_reports[user]['paid']
            result.user_reports[user]['result']['should_get'] = diff > 0
            result.user_reports[user]['result']['value'] = abs(diff)

        return render(request, 'reports/project_report.html', {'costs': costs, 'result': result})

    def post(self, request):
        costs = []
        for cost_id in request.POST.getlist('cost_ids'):
            cost_record = get_object_or_404(CostRecord, id=cost_id)
            cost_record.calculated = True
            cost_record.save()
            costs.append(cost_record)

        return render(request, 'reports/final_project_report.html', {'costs': costs})