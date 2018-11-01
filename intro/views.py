import requests

# Create your views here.
from django.views.generic import TemplateView

from intro.utils import toPersianDigit


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        registration_url = "http://ssc.ce.sharif.edu/pages/payment-forms/interna2018/?successful_payment_count=true"
        content = requests.get(registration_url).text
        return {"numberOfTeams":toPersianDigit(content)}
