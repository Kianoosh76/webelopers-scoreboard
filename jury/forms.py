from django.forms.fields import BooleanField
from django.forms.models import ModelForm

from features.models import Attempt
from jury.models import JudgeRequestAssignment


class JudgingForm(ModelForm):
    class Meta:
        model = JudgeRequestAssignment
        fields = ['score', 'is_passed', 'is_closed']

    is_closed = BooleanField(required=False)

    def save(self, **kwargs):
        instance = super().save(**kwargs)

        is_closed = self.cleaned_data.get('is_closed')
        if instance.judge_request.assignees.filter(score__isnull=False).count() > 1:
            is_closed = True
        instance.judge_request.is_closed = is_closed
        instance.judge_request.save()
        return instance