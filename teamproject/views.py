from django.shortcuts import redirect, render
from django.utils import timezone
from teamproject.models import *
from accounts.models import *
from hackathon.models import *

from teamproject import parseGit
import subprocess
import os

# Create your views here.
def main(request, teamId):
    if not 'memberId' in request.session:
        return redirect('/lobby')
    else:
        return render(request, 'teamproject/main.html', {
            'memberId':request.session['memberId'],
            'teamId':teamId,
            'team':Team.objects.get(pk=teamId),
        })

def notice(request, teamId):
    if not 'memberId' in request.session:
        return redirect('/lobby')
    else:
        memberId = request.session['memberId']
        member = Member.objects.get(pk=memberId)
        team = Team.objects.get(pk=teamId)
        participate = Participate.objects.get(memberId=member, teamId=team)
        hackathon = participate.hackId;

        hasHackathon = True
        teamNotices = TeamNotice.objects.filter(teamId = team)
        hackNotices = []

        if hackathon is None:
            hasHackathon = False;
        else :
            hackNotices = HackNotice.objects.filter(hackId = hackathon)
        return render(request, 'teamproject/notice.html', {
            'memberId':memberId,
            'teamId':teamId,
            'team': team,
            'hasHackathon':hasHackathon,
            'teamNotices':teamNotices,
            'hackNotices':hackNotices,
        })

def contribution(request, teamId):
    if not 'memberId' in request.session:
        return redirect('/lobby')
    else:
        memberId = request.session['memberId']
        member = Member.objects.get(pk=memberId)
        team = Team.objects.get(pk=teamId)
        teamContribution = TeamContribution.objects.get(teamId = team)

        participate = Participate.objects.get(memberId=member, teamId=team)
        hackName = memberId
        if participate.hackId is not None:
            hackName = participate.hackId.pk

        resourceList = ["jpg", "png"]
        current_path = os.getcwd()
        parsingData = parseGit.parseGit(hackName, team.teamName, "", resourceList)
        os.chdir(current_path)
        print("@@@@ hackName: " + hackName)
        print("@@@@ teamName: " + team.teamName)

        contributions = {}
        etcContribution = {'memberId':'etc', 'code':0, 'comment':0, 'resource':0, 'total':0}

        participate = Participate.objects.filter(teamId=team)
        for p in participate:
            newContribution = {'memberId':p.memberId.memberId, 'code':0, 'comment':0, 'resource':0, 'total':0}
            contributions[p.memberId.memberId] = newContribution

        for commit in parsingData:
            author = commit['author']
            if author in contributions:
                contributions[author]['code']     += commit['code']
                contributions[author]['comment']  += commit['comment']
                contributions[author]['resource'] += commit['resource']
            else :
                etcContribution['code']     += commit['code']
                etcContribution['comment']  += commit['comment']
                etcContribution['resource'] += commit['resource']

        contributions['etc'] = etcContribution
        for con in contributions.values():
            con['total'] = con['code'] * teamContribution.code + con['comment'] * teamContribution.comment + con['resource'] * teamContribution.resource

        return render(request, 'teamproject/contribution.html', {
            'memberId':memberId,
            'teamId':teamId,
            'team':team,
            'comment':teamContribution.comment,
            'code':teamContribution.code,
            'resource':teamContribution.resource,
            'contributions':contributions.values,
            'test': contributions,
        })

def chat(request, teamId):
    if not 'memberId' in request.session:
        return redirect('/lobby')
    else:
        team = Team.objects.get(pk=teamId)
        chatMsgs = TeamChat.objects.filter(teamId = team)
        return render(request, 'teamproject/chat.html', {
            'memberId':request.session['memberId'],
            'teamId':teamId,
            'team':team,
            'chatMsgs':chatMsgs,
        })

def member(request, teamId):
    if not 'memberId' in request.session:
        return redirect('/lobby')
    else:
        return render(request, 'teamproject/member.html', {
            'memberId':request.session['memberId'],
            'teamId':teamId,
            'team':Team.objects.get(pk=teamId),
        })

# TODO: create view에서 해커톤 아이디랑 이름 받아와서 해커톤 가능하게 할 수 있겠다.
def create(request):
    if not 'memberId' in request.session:
        return redirect('/lobby')
    else:
        return render(request, 'teamproject/create.html', {
            'memberId':request.session['memberId'],
        })

def createWithHackId(request, hackId):
    if not 'memberId' in request.session:
        return redirect('/lobby')
    else:
        hackTitle = HackathonInformation.objects.get(pk=hackId).title
        return render(request, 'teamproject/create.html', {
            'memberId':request.session['memberId'],
            'hackTitle':hackTitle,
            'hackId':hackId
        })
def process_create(request):

    # exception
    if not 'memberId' in request.session:
        return redirect('/lobby')
    if request.method == 'GET':
        return redirect('/lobby')

    leaderId = request.session['memberId']
    teamName = request.POST['teamName']
    hackId = request.POST['hackId']
    leader = Member.objects.filter(memberId=leaderId)[0]

    team = Team.objects.create(teamName=teamName, leaderId=leader)
    team.save()

    teamContribution = TeamContribution.objects.create(teamId=team)
    teamContribution.save()

    if hackId != "":
        hackathon = HackathonInformation.objects.get(id=hackId)
        # 삭제하고 다시 생성하는 과정!
        Participate.objects.get(memberId = leader, hackId = hackathon).delete()
        participate = Participate.objects.create(memberId=leader, teamId=team, hackId=hackathon)
        participate.save()
        subprocess.call ('/home/pi/remote/remote.sh ' + hackId + ' ' + teamName, shell=True)
    else:
        participate = Participate.objects.create(memberId=leader, teamId=team)
        participate.save()
        subprocess.call ('/home/pi/remote/remote.sh ' + leaderId + ' ' + teamName, shell=True)
    return redirect('/lobby')

def team_notice_post(request, teamId):

    # exception
    if not 'memberId' in request.session:
        return redirect('/lobby')
    if request.method == 'GET':
        return redirect('/lobby')

    writerId = request.session['memberId']

    writer = Member.objects.get(pk=writerId)
    team = Team.objects.get(pk=teamId)
    title = request.POST['title']
    content = request.POST['content']

    notice = TeamNotice.objects.create(title=title, teamId=team, content=content, writer=writer)
    notice.post()
    return redirect('./notice')

def team_notice_view(request, teamId, noticeId):

    # exception
    if not 'memberId' in request.session:
        return redirect('/lobby')

    memberId = request.session['memberId']
    noticeType = 'team'
    notice = TeamNotice.objects.get(pk=noticeId)

    return render(request, 'teamproject/notice_view.html', {
        'memberId':memberId,
        'noticeType':noticeType,
        'notice':notice,
    })
def hack_notice_view(request, teamId, noticeId):
    # exception
    if not 'memberId' in request.session:
        return redirect('/lobby')

    memberId = request.session['memberId']
    noticeType = 'hackathon'
    notice = TeamNotice.objects.get(pk=noticeId)

    return render(request, 'teamproject/notice_view.html', {
        'memberId':memberId,
        'noticeType':noticeType,
        'notice':notice,
    })
