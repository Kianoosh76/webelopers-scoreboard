from django.contrib import admin
from jet.admin import CompactInline

from WSS.models import WSS


class WSSAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'start_date', 'end_date')

admin.site.register(WSS, WSSAdmin)
