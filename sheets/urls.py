from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'sheets'
urlpatterns = [
    url(r'^costs$', login_required(views.CostListView.as_view()), name='cost-list'),
    url(r'^costs/add$', login_required(views.AddCostView.as_view()), name='add-costs'),
    url(r'^cost/(?P<pk>\d+)$', login_required(views.CostDetailView.as_view()), name="cost-details"),
    url(r'^cost/(?P<pk>\d+)/update$', login_required(views.CostUpdateView.as_view()), name='update-cost'),
    url(r'^cost/(?P<pk>\d+)/delete$', login_required(views.CostDeleteView.as_view()), name='delete-cost')
]