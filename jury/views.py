from django.contrib.admindocs.views import TemplateDetailView
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView

from jury.forms import JudgingForm
from jury.models import JudgeRequest, JudgeRequestAssignment, AutomatedJudge
from webelopers_scoreboard.helpers import get_client_ip


class JudgingView(UpdateView):
    form_class = JudgingForm
    template_name = 'judging.html'
    success_url = reverse_lazy('jury:judge-requests')

    def get_object(self, queryset=None):
        return JudgeRequestAssignment.objects.get(judge=self.request.user.judge,
                                                  judge_request=self.kwargs['pk'])

class AutomatedJudgingView(UpdateView):
    model = JudgeRequestAssignment
    http_method_names = ['post']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        judge = AutomatedJudge.objects.get(ip_address=get_client_ip(self.request))
        return get_object_or_404(self.model, score=None, judge=judge,
                                 judge_request__team__id=self.request.POST['group_id'])

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        if request.POST['verdict'] == 'ok':
            object.score = object.judge_request.feature.score
            object.is_passed = True
        else:
            object.score = 0
            object.is_passed = False
        object.message = request.POST['log']
        object.judge_request.is_closed = True
        object.judge_request.save()
        object.save()
        return HttpResponse()


class JudgeRequestsListView(ListView):
    model = JudgeRequest
    template_name = 'judge_requests_list.html'
    context_object_name = 'judge_requests'

    def get_queryset(self):
        queryset = JudgeRequest.objects.all().annotate(count=Count('assignees')).order_by('-time')
        user_assignments = self.request.user.judge.assignments.all().order_by('-judge_request__time')

        self.filter = self.request.GET.get('filter', 'unassigned')
        if self.filter == 'unassigned':
            queryset = queryset.filter(is_closed=False, count__lt=2)
            y = []
            for x in queryset:
                if not JudgeRequestAssignment.objects.filter(judge_request=x,
                                                             judge=self.request.user.judge).exists():
                    y += [x]
            queryset = y
        elif self.filter == 'todo':
            user_assignments = user_assignments
            queryset = [x.judge_request for x in user_assignments.filter(score=None)]
        elif self.filter == 'past':
            user_assignments = user_assignments
            queryset = [x.judge_request for x in user_assignments.filter(score__isnull=False)]
        elif self.filter == 'closed':
            queryset = queryset.filter(is_closed=True)
        return queryset

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'filter': self.filter}


class AssignView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('jury:judge-requests') + '?filter=todo'

    def get(self, request, *args, **kwargs):
        judge_request = JudgeRequest.objects.get(id=int(kwargs['pk']))
        if judge_request.is_closed or judge_request.assignees.count() > 1:
            raise PermissionError()
        JudgeRequestAssignment.objects.get_or_create(judge=self.request.user.judge,
                                                     judge_request_id=int(kwargs['pk']))
        return super().get(request, *args, **kwargs)


class DeassignView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('jury:judge-requests') + '?filter=todo'

    def get(self, request, *args, **kwargs):
        if JudgeRequest.objects.get(id=int(kwargs['pk'])).is_closed:
            raise PermissionError()
        assignment = JudgeRequestAssignment.objects.get(
            judge_request_id=int(kwargs['pk']), judge=self.request.user.judge)
        if assignment.score == None:
            assignment.delete()
        return super().get(request, *args, **kwargs)
