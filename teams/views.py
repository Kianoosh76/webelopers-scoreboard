import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.views.generic.edit import CreateView
from django.conf import settings

from jury.models import JudgeRequestAssigment, Judge
from teams.forms import JudgeRequestForm


# https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django?rq=1
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class JudgeRequestView(LoginRequiredMixin, CreateView):
    form_class = JudgeRequestForm
    template_name = 'judge_request.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['judge_requests'] = self.request.user.team.judge_requests.order_by('-time')[:10]
        return context

    def get_success_url(self):
        return reverse('teams:judge-request')

    def form_valid(self, form):
        data = {
            'group_id': self.request.user.team.pk,
            'ip': get_client_ip(self.request),
            'test_order': '{' + form.data['feature'] + '}'
        }
        response = requests.post('http://' + settings.TESTER_URL + ":" + settings.TESTER_PORT, data)
        if response.status_code != 200:
            form.add_error('feature', response.content)
            return super().form_invalid(form)
        else:
            ret = super().form_valid(form)
            JudgeRequestAssigment.objects.create(score=None, judge_request=form.instance, judge=Judge.get_automated())
            return ret

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), 'request': self.request.user.team}