from django.shortcuts import render, get_object_or_404
from django.views import View

from sheets.models import CostRecord


class ProjectReportView(View):
    def get(self, request):
        proj = request.user.current_project
        costs = CostRecord.objects.filter(project=proj).filter(calculated=False)

        result = self._calculate_report(costs, proj)

        return render(
            request,
            'reports/project_report.html',
            {'costs': costs, 'result': result, 'confirmed': False}
        )

    def post(self, request):
        costs = []
        for cost_id in request.POST.getlist('cost_ids'):
            cost_record = get_object_or_404(CostRecord, id=cost_id)
            cost_record.calculated = True
            cost_record.save()
            costs.append(cost_record)

        proj = request.user.current_project
        result = self._calculate_report(costs, proj)

        return render(
            request,
            'reports/project_report.html',
            {'costs': costs, 'result': result, 'confirmed': True}
        )

    def _calculate_report(self, costs, proj):
        result = {'sum': 0, 'user_reports': {}}

        for user in proj.members.all():
            result['user_reports'][user] = {
                'responsibility': proj.projectmembership_set.get(user=user).rate,
                'paid': 0,
                'should_pay': 0,
                'result': {
                    'should_get': True,
                    'value': 0
                }
            }

        for cost in costs:
            result['sum'] += cost.cost
            result['user_reports'][cost.payer]['paid'] += cost.cost

        total_responsibilities = 0
        for user in result['user_reports'].values():
            total_responsibilities += user['responsibility']

        for user in result['user_reports'].keys():
            user_report = result['user_reports'][user]
            user_report['should_pay'] = result['sum'] * user_report['responsibility'] / total_responsibilities
            diff = user_report['should_pay'] - user_report['paid']
            user_report['result']['should_get'] = diff < 0
            user_report['result']['value'] = abs(diff)

        return result