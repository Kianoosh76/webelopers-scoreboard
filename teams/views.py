from threading import Timer

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.views.generic.edit import CreateView

from jury.models import JudgeRequestAssignment, Config, AutomatedJudge
from teams.forms import JudgeRequestForm
from webelopers_scoreboard.helpers import get_client_ip


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
        if not Config.get_solo().assign_to_automated_judge:
            return super().form_valid(form)

        data = {
            'group_id': self.request.user.team.pk,
            'ip': get_client_ip(self.request),
            'test_order': int(form.cleaned_data['feature'].name),
            'port': 8000,
        }
        assigned_judge = AutomatedJudge.get_random_judge()
        try:
            response = requests.post('http://' + assigned_judge.ip_address + ":" + str(assigned_judge.port), data, timeout=30)
        except Exception as exc:
            form.add_error('feature', str(exc))
            return super().form_invalid(form)

        if response.status_code != 200:
            form.add_error('feature', response.content)
            return super().form_invalid(form)
        else:
            ret = super().form_valid(form)
            assignment = JudgeRequestAssignment.objects.create(score=None, judge_request=form.instance, judge=assigned_judge)
            def timeout():
                assignment.refresh_from_db()
                if assignment.score is None:
                    assignment.score = 0
                    assignment.is_passed = False
                    assignment.message = 'Request has been timed out.'
                    assignment.save()
                    assignment.judge_request.is_closed = True
                    assignment.judge_request.save()
            Timer(Config.get_solo().timeout_minutes * 60, timeout).start()
            return ret

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), 'request': self.request.user.team}
