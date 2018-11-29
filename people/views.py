from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# from WSS.mixins import FooterMixin
from people.models import TechnicalExpert


class CreatorsListView(ListView):
    model = TechnicalExpert
    template_name = 'people/creators_list.html'
    context_object_name = 'technical_experts'


class StaffListView(DetailView):
    template_name = 'people/staff_list.html'