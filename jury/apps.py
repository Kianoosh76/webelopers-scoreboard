from bs4 import BeautifulSoup
from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save, pre_save

from django.test.client import Client
from django.urls import reverse


def update_corresponding_attempt(sender, instance, created, **kwargs):
    if created:
        return

    from features.models import Attempt

    attempt, _ = Attempt.objects.get_or_create(team=instance.judge_request.team,
                                               feature=instance.judge_request.feature)
    attempt.score = instance.judge_request.score
    attempt.is_passed = instance.judge_request.is_passed
    attempt.save()


def freeze_handler(sender, instance, **kwargs):
    if instance.is_frozen and not instance.frozen_scoreboard:
        client = Client()
        response = BeautifulSoup(client.get(reverse('features:scoreboard')).content, 'html.parser')
        instance.frozen_scoreboard = str(response.find(id=settings.FROZEN_SCOREBOARD_TAG))
    elif not instance.is_frozen and instance.frozen_scoreboard:
        instance.frozen_scoreboard = ""


class JuryConfig(AppConfig):
    name = 'jury'

    def ready(self):
        from jury.models import JudgeRequestAssignment, Config
        post_save.connect(update_corresponding_attempt, sender=JudgeRequestAssignment)
        pre_save.connect(freeze_handler, sender=Config)
