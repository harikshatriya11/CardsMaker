from django.contrib import admin

# Register your models here.
from sports.TBT11.tbt.models import *

from import_export.admin import ImportExportModelAdmin


class DynamicListDisplayAdmin(admin.ModelAdmin):
    def get_model_fields(self, model):
        return [field.name for field in model._meta.get_fields()]

    def get_list_display(self, request):
        model = self.model
        fields = self.get_model_fields(model)
        return fields


class DynamicListDisplayAdmin(admin.ModelAdmin):
    def get_model_fields(self, model):
        return [field.name for field in model._meta.get_fields()]

    def get_list_display(self, request):
        model = self.model
        fields = self.get_model_fields(model)
        return fields


class MainDynamicListDisplayAdmin(admin.ModelAdmin):
    def get_model_fields(self, model):
        return [field.name for field in model._meta.get_fields()]

    def get_list_display(self, request):
        model = self.model
        fields = self.get_model_fields(model)
        return fields



class PlayerAdmin(ImportExportModelAdmin):
    search_fields=['full_name']
class TeamAdmin(ImportExportModelAdmin):
    pass



admin.site.register(Profile, DynamicListDisplayAdmin)
admin.site.register(UserPDetails, DynamicListDisplayAdmin)
# admin.site.register(cbdkg)
admin.site.register(Sport, DynamicListDisplayAdmin)
admin.site.register(Cup)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match)
admin.site.register(Contest)
admin.site.register(CreatedTeam)
admin.site.register(JoinedContest, DynamicListDisplayAdmin)
admin.site.register(CricketPlayerLivePoint)
admin.site.register(TransactionHistory, DynamicListDisplayAdmin)
admin.site.register(AccountBalance)
admin.site.register(HelpAndSupport, DynamicListDisplayAdmin)
admin.site.register(AndroidApp, DynamicListDisplayAdmin)
admin.site.register(BankDetails, DynamicListDisplayAdmin)



admin.site.register(RequestedWithdrawal, DynamicListDisplayAdmin)

