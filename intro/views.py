import requests

# Create your views here.
from django.views.generic import TemplateView

from intro.models import Staff
from intro.utils import toPersianDigit


class HomeView(TemplateView):
    template_name = 'intro/home.html'

    def get_context_data(self, *args, **kwargs):
        registration_url = "http://ce.sharif.edu/~golezardi/ssc-count/webelopers.php"
        content = requests.get(registration_url).text
        return {"numberOfTeams":toPersianDigit(content)}

class StaffView(TemplateView):
    template_name = 'intro/staff_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staffs'] = Staff.objects.all().order_by('?')

        return context
