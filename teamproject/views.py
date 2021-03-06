from django.shortcuts import render, reverse, HttpResponseRedirect, redirect
from django.utils import timezone
from teamproject.models import *
from accounts.models import *
from hackathon.models import *

from teamproject import parseGit
from teamproject import gitBranch
import subprocess
import os

# Create your views here.
def main(request, teamId):
    if not 'memberId' in request.session:
        return redirect('/lobby')
    else:

        memberId = request.session['memberId']
        team = Team.objects.get(pk=teamId)
        teamMembers = Participate.objects.filter(teamId = team)
        teamLeader = team.leaderId
        leaderParticipate = Participate.objects.get(memberId=teamLeader, teamId=team)
        leaderHack = leaderParticipate.hackId

        # merge request part
        mergeResponse = []
        teamMergeRequests = TeamMergeRequest.objects.filter(teamId = team)
        for teamMergeRequest in teamMergeRequests:
            mergeData = {}
            mergeData['requestId'] = teamMergeRequest.pk
            mergeData['fromBranch'] = teamMergeRequest.fromBranch
            mergeData['toBranch'] = teamMergeRequest.toBranch
            mergeData['agree'] = 0
            mergeData['disagree'] = 0
            mergeData['canMerge'] = False
            teamVotes = TeamVote.objects.filter(requestId = teamMergeRequest)
            for teamVote in teamVotes:
                if teamVote.isAgree == True:
                    mergeData['agree'] += 1
                else:
                    mergeData['disagree'] += 1
            if mergeData['agree'] >= len(teamMembers)/2:
                mergeData['canMerge'] = True
            mergeResponse.append(mergeData)

        #branch list
        hackName = teamLeader.memberId
        if leaderHack is not None:
            hackName = leaderHack.pk
        parsingData = gitBranch.showAllRemoteBranch(hackName, team.teamName)

        return render(request, 'teamproject/main.html', {
            'memberId':request.session['memberId'],
            'teamId':teamId,
            'team':Team.objects.get(pk=teamId),
            'mergeData':mergeResponse,
            'name': 'main',
            'branchData':parsingData,
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
            'name': 'notice',
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

        commits = Commit.objects.filter(teamId=team)

        contributions = {}
        etcContribution = {'memberId':'#etc', 'code':0, 'comment':0, 'resource':0, 'total':0}

        participate = Participate.objects.filter(teamId=team)
        for p in participate:
            newContribution = {'memberId':p.memberId.memberId, 'code':0, 'comment':0, 'resource':0, 'total':0}
            contributions[p.memberId.memberId] = newContribution

        if True: # error exception
            for commit in commits:
                author = commit.author
                if author in contributions:
                    contributions[author]['code']     += commit.code
                    contributions[author]['comment']  += commit.comment
                    contributions[author]['resource'] += commit.resource
                else :
                    etcContribution['code']     += commit.code
                    etcContribution['comment']  += commit.comment
                    etcContribution['resource'] += commit.resource

            contributions['#etc'] = etcContribution
            totalContribution = 0.0
            for con in contributions.values():
                con['total'] = con['code'] * teamContribution.code + con['comment'] * teamContribution.comment + con['resource'] * teamContribution.resource
                totalContribution += con['total']

            if totalContribution == 0.0:

                totalContribution = 1

            for con in contributions.values():
                con['total'] = con['total']/totalContribution * 100

        return render(request, 'teamproject/contribution.html', {
            'memberId':memberId,
            'teamId':teamId,
            'team':team,
            'comment':teamContribution.comment,
            'code':teamContribution.code,
            'resource':teamContribution.resource,
            'contributions':contributions.values(),
            'test': contributions,
            'name': "contribution",
        })

def contribution_save(request, teamId):
    if request.method == 'GET':
        return redirect('/lobby')
    if not 'memberId' in request.session:
        return redirect('/lobby')
    else:
        memberId = request.session['memberId']
        member = Member.objects.get(pk=memberId)
        team = Team.objects.get(pk=teamId)
        teamContribution = TeamContribution.objects.get(teamId = team)

        try:
            comment = float(request.POST['comment'])
            code = float(request.POST['code'])
            resource = float(request.POST['resource'])
            teamContribution.comment = comment
            teamContribution.code = code
            teamContribution.resource = resource
            teamContribution.save()
        except:
            print('float parsing err')
        return redirect('./contribution')

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
            'name': 'chat',
        })

def member(request, teamId):
    if not 'memberId' in request.session:
        return redirect('/lobby')
    else:
        memberId = request.session['memberId']
        member = Member.objects.get(memberId=memberId)
        team = Team.objects.get(pk=teamId)
        leader = team.leaderId

        if member != leader:
            redirect_to = reverse('main', kwargs={'teamId':teamId})
            return HttpResponseRedirect(redirect_to)
        else:
            memberList = Member.objects.filter(participate__teamId = team)
            if request.method == 'POST':
                selectedMemberId = request.POST['memberId']
                selectedMember = Member.objects.get(memberId=selectedMemberId)
                #리더를 삭제 -> 금지
                if selectedMember == leader:
                    redirect_to = reverse('main', kwargs={'teamId':teamId})
                    return HttpResponseRedirect(redirect_to)
                else:
                    teamId = request.POST['teamId']
                    team = Team.objects.get(pk=teamId)
                    participate = Participate.objects.filter(memberId = selectedMember, teamId = team)
                    participate.update(teamId=None)
                    memberList = Member.objects.filter(participate__teamId = team)

        return render(request, 'teamproject/member.html', {
            'memberId':request.session['memberId'],
            'teamId':teamId,
            'team':team,
            'name': 'member',
            'memberList':memberList,
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
        old_path = os.getcwd()
        subprocess.call ('/home/pi/remote/remote.sh ' + hackId + ' ' + teamName, shell=True)
        os.chdir(old_path)
    else:
        participate = Participate.objects.create(memberId=leader, teamId=team)
        participate.save()
        old_path = os.getcwd()
        subprocess.call ('/home/pi/remote/remote.sh ' + leaderId + ' ' + teamName, shell=True)
        os.chdir(old_path)
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
    teamId = teamId

    return render(request, 'teamproject/notice_view.html', {
        'memberId':memberId,
        'noticeType':noticeType,
        'notice':notice,
        'teamId':teamId,
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

def merge_request(request, teamId):

    # exception
    if not 'memberId' in request.session:
        return redirect('/lobby')

    memberId = request.session['memberId']
    fromBranch = request.POST['fromBranch']
    toBranch = request.POST['toBranch']
    print(fromBranch)
    print(toBranch)

    team = Team.objects.get(pk=teamId)
    teamMergeRequest = TeamMergeRequest.objects.create(teamId = team, fromBranch = fromBranch, toBranch = toBranch)
    teamMergeRequest.save()
    return redirect('./main')

def vote_agree(request, teamId):

    # exception
    if not 'memberId' in request.session:
        return redirect('/lobby')

    memberId = request.session['memberId']
    requestId = request.POST['requestId']

    member = Member.objects.get(memberId=memberId)
    teamMergeRequest = TeamMergeRequest.objects.get(pk=requestId)
    teamVote = TeamVote.objects.filter(requestId = teamMergeRequest, memberId=member)
    if len(teamVote) == 0:
        teamVote = TeamVote.objects.create(requestId = teamMergeRequest, memberId = member)
        teamVote.save()
    else:
        teamVote[0].isAgree = True
        teamVote[0].save()
    return redirect('./main')

def vote_disagree(request, teamId):

    # exception
    if not 'memberId' in request.session:
        return redirect('/lobby')

    memberId = request.session['memberId']
    requestId = request.POST['requestId']

    member = Member.objects.get(memberId=memberId)
    teamMergeRequest = TeamMergeRequest.objects.get(pk=requestId)
    teamVote = TeamVote.objects.filter(requestId = teamMergeRequest, memberId=member)
    if len(teamVote) == 0:
        teamVote = TeamVote.objects.create(requestId = teamMergeRequest, memberId = member)
        teamVote.save()
    else:
        teamVote[0].isAgree = False
        teamVote[0].save()
    return redirect('./main')

def merge(request, teamId):

    # exception
    if not 'memberId' in request.session:
        return redirect('/lobby')

    memberId = request.session['memberId']
    requestId = request.POST['requestId']

    teamMergeRequest = TeamMergeRequest.objects.get(pk=requestId)
    teamMergeRequest.delete()
    return redirect('./main')
