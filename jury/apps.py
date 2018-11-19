from django.apps import AppConfig
from django.db.models.signals import post_save


def update_corresponding_attempt(sender, instance, created, **kwargs):
    if created:
        return

    from features.models import Attempt

    attempt, _ = Attempt.objects.get_or_create(team=instance.judge_request.team,
                                               feature=instance.judge_request.feature)
    attempt.score = instance.judge_request.score
    attempt.is_passed = instance.judge_request.is_passed
    attempt.save()


class JuryConfig(AppConfig):
    name = 'jury'

    def ready(self):
        from jury.models import JudgeRequestAssignment
        post_save.connect(update_corresponding_attempt, sender=JudgeRequestAssignment)
