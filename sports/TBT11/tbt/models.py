import datetime
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from choice import *

from sports.TBT11.choice import TANSACTION_STATUS_CHOICES, CRICKET_PLAYER_PLACE_CHOICES, Played_last_match_CHOICES


class Profile(models.Model):
    profile_user_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profile_user_name')
    address = models.CharField(default="", max_length=145)
    contact1 = models.CharField(default="", max_length=15)
    contact2 = models.CharField(default="", max_length=15)
    dialcode =  models.CharField(default="", max_length=15)
    image = models.ImageField(upload_to='profile', blank=True)
    firebase_uid = models.CharField(default="", max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.profile_user_name)
class UserPDetails(models.Model):
    firebase_uid = models.CharField(default="", max_length=100)
    user_kmt = models.CharField(default="", max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.firebase_uid)
class AccountBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='aacount_balance_username')
    bonus = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    widthdrawal = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    deposit = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    widthdrawn = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.user)
class BankDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='bank_details')
    upi = models.CharField(default="", max_length=50)
    card_number = models.CharField(default="", max_length=50)
    card_type = models.CharField(default="", max_length=50)
    adhaar = models.CharField(default="", max_length=50)
    bank_account_number = models.CharField(default="", max_length=50)
    bank_name = models.CharField(default="", max_length=50)
    bank_ifsc_code = models.CharField(default="", max_length=50)
    address = models.CharField(default="", max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.user)
class TransactionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='transaction_history_username')
    bonus = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    widthdrawal = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    deposit = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    widthdrawn = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    status = models.CharField(max_length=1, choices=TANSACTION_STATUS_CHOICES, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # widthrawaal = models.DecimalField(default=0.00, max_digits=10)
    def __str__(self):
        return '{}'.format(self.user)
class Sport(models.Model):
    sport_name = models.CharField(default="", max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.sport_name)
class Cup(models.Model):
    cup_name = models.CharField(default="", max_length=100)
    category = models.CharField(default="", max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, null=True, blank=True, related_name='cup_sport')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.cup_name)

class Team(models.Model):
    name = models.CharField(default="", max_length=50)
    name_abr = models.CharField(default="", max_length=20)
    team_sport = models.ForeignKey(Sport, on_delete=models.CASCADE, null=True, blank=True, related_name='team_sport')
    country = models.CharField(default="", max_length=100)
    team_id = models.CharField(default="", max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.name)


class Player(models.Model):
    full_name = models.CharField(default="", max_length=100)
    abr_name = models.CharField(default="", max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, null=True, blank=True, related_name='game')
    player_place = models.CharField(max_length=1, choices=CRICKET_PLAYER_PLACE_CHOICES, default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='team')
    country = models.CharField(default="", max_length=100)
    country_abr = models.CharField(default="", max_length=100)
    image = models.ImageField(upload_to='players',default='cricket_profile.jpeg',blank=True)
    status = models.BooleanField(default=False)
    in_squad = models.BooleanField(default=False)
    played_last_match = models.CharField(max_length=20, choices=Played_last_match_CHOICES, default=0)
    credit_point = models.PositiveIntegerField(default=7)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.full_name)

class Match(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    cup =  models.ForeignKey(Cup, on_delete=models.CASCADE, null=True, blank=True, related_name='Cup')
    team1 =  models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='team1')
    team2 =  models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='team2')
    place =  models.CharField(default="", max_length=100)
    won_by =  models.CharField(default="", max_length=100)
    date =  models.DateField(blank=True, null=True)
    time =  models.TimeField(blank=True, null=True)
    cric_id = models.IntegerField(default=1)
    cric_url = models.CharField(default='',max_length=200,)
    active = models.BooleanField(default=True)
    end = models.BooleanField(default=False)
    end_time =  models.TimeField(blank=True, null=True)
    announced = models.BooleanField(default=False)
    live = models.BooleanField(default=False)
    def __str__(self):

        return '{}'.format(str(self.team1) +" Vs "+ str(self.team2))
class MatchScoreBoard(models.Model):
    match =  models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True, related_name='Cup')
    inning_1st_batting =  models.CharField(default="", max_length=100)
    inning_2st_batting =  models.CharField(default="", max_length=100)
    active = models.BooleanField(default=True)
    def __str__(self):

        return '{}'.format(str(self.match))

class CricketPlayerLivePoint(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True, related_name='player_live_point')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True, related_name='match_live_point')
    announced = models.BooleanField(default=False)
    insquad = models.BooleanField(default=False, null=True)
    run = models.IntegerField(default=0)
    ball = models.IntegerField(default=0)
    four = models.IntegerField(default=0)
    six = models.IntegerField(default=0)
    strike_runrate = models.FloatField(default=0)
    run_bonus = models.IntegerField(default=0)
    duck = models.IntegerField(default=0)
    wicket = models.IntegerField(default=0)
    wicket_bonus = models.IntegerField(default=0)
    lbw_bowled_bonus =  models.IntegerField(default=0)
    maiden_over =  models.IntegerField(default=0)
    economy =  models.FloatField(default=0)
    catch =  models.IntegerField(default=0)
    catch_bonus =  models.IntegerField(default=0)
    runout_stumping =  models.IntegerField(default=0)
    better_of_the_team = models.BooleanField(default=False)
    Lcaptain = models.BooleanField(default=False)
    Lvice_captain = models.BooleanField(default=False)
    total =  models.FloatField(default=0)
    def __str__(self):
        if self.announced:

            playing = 4
            total_point = self.run+playing+ self.four*1 + self.six*2 +self.wicket*25 + self.wicket_bonus*2 + self.catch*8+self.catch_bonus*1+self.runout_stumping*12
            CricketPlayerLivePoint.objects.filter(id=self.id).update(total = int(total_point))
        else: total_point = 0
        if self.captain:
            total_point*2
        elif self.vice_captain:
            total_point*1.5

        return '{}'.format(str(self.player) + "-"+str(total_point))

class Contest(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_by')
    match_contest = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True, related_name='Match_contest')
    contest_name = models.CharField(default="", max_length=100)
    prize_pool = models.CharField(default="", max_length=100)
    prize_distribution = models.CharField(default="{}", max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    entry_fee = models.CharField(default="free", max_length=100)
    entry_fee_value = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    limit = models.PositiveIntegerField(default=0)
    team_limit = models.PositiveIntegerField(default=1)
    live = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.contest_name)

class CreatedTeam(models.Model):
    username_ct = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='username_ct')
    TeamCount = models.PositiveIntegerField(default=1)
    player1 = models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='player1')
    player2 = models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='player2')
    player3 = models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='player3')
    player4 = models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='player4')
    player5 = models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='player5')
    player6 = models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='player6')
    player7 = models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='player7')
    player8 = models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='player8')
    player9 = models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='player9')
    player10= models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='player10')
    player11= models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='player11')
    captain= models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='captain')
    vice_captain= models.ForeignKey(CricketPlayerLivePoint, on_delete=models.CASCADE, null=True, blank=True, related_name='vice_captain')
    contest_name = models.ForeignKey(Contest, on_delete=models.CASCADE, null=True, blank=True, related_name='name')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True, related_name='created_team_match')
    total_points = models.FloatField(default=0.00,null=True,blank=True)

    def __str__(self):
        # p1 = CricketPlayerLivePoint.objects.get(id=self.player1_id)
        # total = 0 + p1.total
        # total = self.player1_total + self.player2.total + self.player3.total + self.player4.total + self.player5.total + self.player6.total + self.player7.total + self.player8.total + self.player9.total + self.player10.total + self.player11.total
        # creted_team = CreatedTeam.objects.get(id=self.id)
        # creted_team.total_points = total
        # creted_team.save()
        return '{0}'.format(self.username_ct)

class JoinedContest(models.Model):
    joined_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='joined_user')
    contest_name_jc = models.ForeignKey(Contest, on_delete=models.CASCADE, null=True, blank=True, related_name='contest_name_jc')
    selected_team = models.ForeignKey(CreatedTeam, on_delete=models.CASCADE, null=True, blank=True, related_name='created_team_jc')
    team_rank = models.IntegerField(default=1)
    won = models.CharField(default='0', max_length=12)
    prize_distributed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.joined_user.username)

class HelpAndSupport(models.Model):
    user_has = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_has')
    name = models.CharField(default='0', max_length=20)
    email = models.CharField(default='0', max_length=100)
    mobile = models.CharField(default='0', max_length=12)
    message = models.CharField(default='0', max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.name)
class AndroidApp(models.Model):
    apk_file = models.FileField(upload_to='android_apk')
    version_code = models.CharField(default='0', max_length=10,blank=True,null=True)
    version = models.CharField(default='0', max_length=10,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.version_code)

class LiveMatchTeam(models.Model):
    live_match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True, related_name='live_match')
    team1 = models.CharField(default='', blank=True,max_length=50)
    team2 = models.CharField(default='', blank=True,max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.version_code)
