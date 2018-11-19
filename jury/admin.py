from django.contrib import admin
from solo.admin import SingletonModelAdmin

from jury.models import JudgeRequest, JudgeRequestAssignment, Config, HumanJudge, \
    AutomatedJudge


class AssigneeInline(admin.TabularInline):
    model = JudgeRequestAssignment


class JudgeRequestAdmin(admin.ModelAdmin):
    inlines  = [AssigneeInline]


admin.site.register(HumanJudge)
admin.site.register(AutomatedJudge)
admin.site.register(JudgeRequest, JudgeRequestAdmin)
admin.site.register(JudgeRequestAssignment)
admin.site.register(Config, SingletonModelAdmin)
