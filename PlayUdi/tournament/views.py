from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Player, Tournament, Match, Profile,TournamentPlayers, Trophy
# from trophy.models import Trophy
from django.contrib.auth.models import User
from comment.models import Comment

import random
import math
# Create your views here.

def tournament_view(request: HttpRequest):
    tournaments=Tournament.objects.all()
    return render(request, 'tournament/tournaments_home.html',{'tournaments':tournaments})


def tournament_controll(request :HttpRequest, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        tournament_players=TournamentPlayers.objects.filter(tournament_id=tournament_id)

        matches = Match.objects.filter(tournament=tournament)
        # if  tournament.number_of_players !=0 and not matches:        
        #     return HttpResponse(tournament_players)
        # elif matches and tournament.number_of_players ==0:
        #     return redirect( 'tournament:show_tournament_details',tournament_id)

        return redirect( 'tournament:show_tournament_details',tournament_id)


def create_tournament(request : HttpRequest):
    if request.method == 'POST':
        # Get the number of players from the form
        num_players = request.POST['number_of_players'] 
        name= request.POST['name']
        description= request.POST['description']
        game= int(request.POST['game'])
        trophy_for_tournament= int(request.POST['trophy_for_tournament'])
        profile=Profile.objects.get(user=request.user)

        if profile.states =='1':
            return HttpResponse("Youre not Allowed to create a tour")
        # Create a new tournament
        tournament = Tournament.objects.create(name=name , number_of_players=num_players,owner=profile,game=game,trophy_for_tournament=trophy_for_tournament,description=description, winner=None)
        return redirect('tournament:tournament_view')
    return render(request, 'tournament/create_tournament.html',{'Tournament':Tournament})

def select_winner(request:HttpRequest, match_id):

    match = Match.objects.get(id=match_id)

    if request.method == 'POST':
        winner_id = int(request.POST['winner'])
        winner_user = User.objects.get(id=winner_id)

        winner = Profile.objects.get(user=winner_user)

        match.winner = winner
        match.save()

        tournament = match.tournament
        round_matches = Match.objects.filter(tournament=tournament, winner=None)
        
        if match.in_round==1 and not tournament.winner:
            tournament.winner = winner
            trophy = Trophy(tournament=tournament, winner=winner, points=tournament.trophy_for_tournament)

            winner.points += int(trophy.points)
            if winner.points > 500:
                winner.user_rank = 'master'
            elif winner.points > 300:
                winner.user_rank = 'pro'
            else:
                winner.user_rank = 'nor'

            trophy.save()
            winner.save()
        if not round_matches:
            generate_next_round(tournament, match.in_round)
            

            

            
    return redirect('tournament:show_tournament_details', tournament_id=match.tournament.id)


def generate_next_round(tournament, in_round):
    round_matches = Match.objects.filter(tournament=tournament, in_round=in_round)
    winners = [match.winner for match in round_matches]

    rounds = in_round - 1  

    new_matches = []
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            match = Match.objects.create(
                tournament=tournament,
                player1=winners[i],
                player2=winners[i + 1],
                in_round=rounds
            )
            new_matches.append(match)

    return new_matches


def show_tournament_details(request:HttpRequest, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_player = TournamentPlayers.objects.filter(tournament=tournament)
    matches = Match.objects.filter(tournament=tournament)
    comments = Comment.objects.filter(tournament=tournament)
    profile_user = Profile.objects.filter(user=request.user).first()
    trophy = Trophy.objects.filter(tournament=tournament).first()

    if request.method == "POST" and request.user.is_authenticated:
        new_comment = Comment(tournament=tournament, profile=profile_user, content=request.POST["content"])
        new_comment.save()
    match_len = matches.count()
    player_exist = TournamentPlayers.objects.filter(tournament=tournament,player=profile_user).exists()

    rounds:dict = {}
    for match in matches:
        round_number = match.in_round
        if round_number not in rounds:
            rounds[round_number] = []
        rounds[round_number].append(match)
    
    return render(request, 'tournament/tournament_details.html', {'tournament': tournament, 'matches': matches, "match_len":match_len, "comments":comments,"tournament_player":tournament_player, "profile_user":profile_user, "player_exist":player_exist, "trophy":trophy, "rounds":rounds})




def enroll_view(request : HttpRequest,tournament_id):
    tournament=Tournament.objects.get(id=tournament_id)
    if tournament.number_of_players==0:
        return HttpResponse('Full')
    user_profile=Profile.objects.get(user=request.user)
    
    if user_profile.states=='2' :
        return HttpResponse("Not alloed to enroll")
    else :
        if TournamentPlayers.objects.filter(tournament=tournament,player=user_profile).exists():

            return HttpResponse("PLayers is enrolled ")
        else:
            user_enrolled_in=TournamentPlayers(tournament=tournament, player=user_profile) 
            tournament.number_of_players-=1
            tournament.save()
            user_enrolled_in.save()
            if tournament.number_of_players ==0 :
                tournament_players=TournamentPlayers.objects.filter(tournament_id=tournament_id)

                matches = Match.objects.filter(tournament=tournament)
                players = []
                for i in range(len(tournament_players)):           
                    players.append(tournament_players[i].player.user.id)
                
                # Randomly assign players to matches for the first round
                rounds = math.log2(len(players))
                random.shuffle(players)
                matches = []
                for i in range(0, len(players), 2):
                    get_user=User.objects.get(id=players[i])
                    get_user2=User.objects.get(id=players[i+1])
                    players1=Profile.objects.get(user=get_user)
                    players2=Profile.objects.get(user=get_user2)
                    match = Match.objects.create(tournament=tournament, player1=players1, player2=players2, in_round=rounds)
                    matches.append(match)

        return redirect('tournament:show_tournament_details', tournament_id)