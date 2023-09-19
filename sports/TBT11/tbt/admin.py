from django.contrib import admin

# Register your models here.
from sports.TBT11.tbt.models import *

from import_export.admin import ImportExportModelAdmin



class PlayerAdmin(ImportExportModelAdmin):
    search_fields=['full_name']
class TeamAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Profile)
admin.site.register(UserPDetails)
# admin.site.register(cbdkg)
admin.site.register(Sport)
admin.site.register(Cup)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match)
admin.site.register(Contest)
admin.site.register(CreatedTeam)
admin.site.register(JoinedContest)
admin.site.register(CricketPlayerLivePoint)
admin.site.register(TransactionHistory)
admin.site.register(AccountBalance)
admin.site.register(HelpAndSupport)
admin.site.register(AndroidApp)
admin.site.register(BankDetails)

