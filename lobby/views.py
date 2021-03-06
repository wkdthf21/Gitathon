from django.shortcuts import redirect, render
from teamproject.models import *
from accounts.models import Member, Participate
from hackathon.models import *

# Create your views here.
def login(request):
    if not 'memberId' in request.session:
        return render(request, 'lobby/login.html', {
            'numTeamproject' : 3000,
            'numHackathon' : 12345
        })
    else:
        return redirect('/lobby/main')

def main(request):
    if not 'memberId' in request.session:
        return redirect('/lobby')
    else:
        member = Member.objects.filter(memberId=request.session['memberId'])
        joinIds = []
        for id in Participate.objects.filter(memberId=member[0]).values('teamId'):
            joinIds.append(id['teamId'])
        joinTeams = Team.objects.filter(id__in=joinIds)
        # 내 해커톤
        hackList = HackathonInformation.objects.filter(participate__memberId=request.session['memberId'])
        teamNotification = TeamCommitNotification.objects.filter(teamId__in=joinTeams)
        return render(request, 'lobby/main.html', {
            'memberId':request.session['memberId'],
            'teams':joinTeams,
            'hackList':hackList,
            'commitNotifications':teamNotification,
        })

def signup(request):
    return lobby(request)

def join(request):
    return render(request, 'lobby/register.html', {})
