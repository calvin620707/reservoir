from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View


class IndexView(View):
    def get(self, request):
        if request.user.current_project:
            return HttpResponseRedirect(reverse('sheets:add-costs'))

        if request.user.project_set.count() > 0:
            return HttpResponseRedirect(reverse('accounts:my-projects'))

        return HttpResponseRedirect(reverse('accounts:my-new-project'))
