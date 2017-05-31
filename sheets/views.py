from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


@login_required
def add_costs(request):
    if not request.user.current_project:
        return HttpResponseRedirect(reverse('my-projects'))
    return render(request, 'sheets/add_costs.html')
