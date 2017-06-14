from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import CostDetailView, AddCostView

app_name = 'sheets'
urlpatterns = [
    url(r'^costs/add$', login_required(AddCostView.as_view()), name='add-costs'),
    url(r'^cost/(?P<pk>\d+)$', login_required(CostDetailView.as_view()), name="cost-details")
]