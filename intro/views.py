from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# Create your views here.
from django.views.generic import TemplateView

from intro.utils import toPersianDigit


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        registration_url = "http://ssc.ce.sharif.edu/pages/payment-forms/%D8%AB%D8%A8%D8%AA-%D9%86%D8%A7%D9%85-%D8%AF%D8%B1-%D8%B1%D9%88%DB%8C%D8%AF%D8%A7%D8%AF-%D8%A7%DB%8C%D9%86%D8%AA%D8%B1%D9%86%D8%A7/"
        client = Request(registration_url, headers={"User-Agent": "Mozilla/5.0"})
        content = urlopen(client).read()
        soup = BeautifulSoup(content,features="html.parser")
        return {"numberOfTeams":toPersianDigit(soup.find('div', id='valid_count').text)}
