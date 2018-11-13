from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def add_automated_judge(sender, **kwargs):
    from jury.models import Judge
    Judge.objects.get_or_create(name=settings.AUTOMATED_JUDGE_NAME, user=None)


class JuryConfig(AppConfig):
    name = 'jury'

    def ready(self):
        post_migrate.connect(add_automated_judge, sender=self)