import requests

# Create your views here.
from django.views.generic import TemplateView

from intro.utils import toPersianDigit


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        registration_url = "http://ce.sharif.edu/~golezardi/ssc-count/webelopers.php"
        content = requests.get(registration_url).text
        return {"numberOfTeams":toPersianDigit(content)}
