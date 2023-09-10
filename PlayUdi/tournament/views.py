from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Player, Tournament, Match,Profile,TournamentPlayers
from django.contrib.auth.models import User
from comment.models import Comment

import random
import math
# Create your views here.

def tournament_view(request: HttpRequest):
    tourments=Tournament.objects.all()

    return render(request, 'tournament/tournaments_home.html',{'touremnts':tourments})


def tournament_controll(request :HttpRequest, tourment_id):
        tournament = Tournament.objects.get(id=tourment_id)
        tournament_players=TournamentPlayers.objects.filter(tourmnet=tournament)

        matches = Match.objects.filter(tournament=tournament)
        if  tournament.number_of_players !=0 and not matches:        
            return HttpResponse(tournament_players)
        elif matches and tournament.number_of_players ==0:
            return render(request, 'tournament/tournaments_home.html', {'tournament': tournament, 'matches': matches})
        



        match_len = matches.count()

        # return HttpResponse(tournament_players[1].player.user.id)
        
            # Create players and matches for the first round
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

        return render(request, 'tournament/tournaments_home.html', {'tournament': tournament, 'matches': matches})


def create_tournament(request : HttpRequest):
    if request.method == 'POST':
        # Get the number of players from the form
        num_players = int(request.POST['num_players']) 
        profile=Profile.objects.get(user=request.user)
        if profile.states =='1':
            return HttpResponse("Youre not Allowed to create a tour")
        # Create a new tournament
        tournament = Tournament.objects.create(name="My Tournament" , number_of_players=num_players,owner=profile)

    return render(request, 'tournament/create_tournament.html')

def select_winner(request, match_id):

    match = Match.objects.get(id=match_id)

    

    if request.method == 'POST':
        winner_id = int(request.POST['winner'])
        winner_user=User.objects.get(id=winner_id)

        winner = Profile.objects.get(user=winner_user)

        # Update the match with the winner
        match.winner = winner
        match.save()
        # Check if all matches in the round have winners
        tournament = match.tournament
        round_matches = Match.objects.filter(tournament=tournament, winner=None)
        

        if not round_matches:
            generate_next_round(tournament, match.in_round)
            # Generate the next round if all matches have winners
            # if is_final_round(tournament):
                # return redirect('tournament:show_tournament', tournament_id=match.tournament.id)
                # matchs = Match.objects.all()
                # for match in matchs:
                #     match.winner = None
                #     match.save()

        if match.in_round==1:
            tournament.is_completed=True
            # winner.add_score 

            tournament.save()

            
    return redirect('tournament:show_tournament', tournament_id=match.tournament.id)

def is_final_round(tournament):
    # Calculate the number of rounds based on the number of players
    num_players = Match.objects.filter(tournament=tournament).count()
    num_rounds = 0
    while num_players > 1:
        num_players = num_players // 2
        num_rounds += 1

    # Calculate the number of rounds that have already been played
    rounds_played = Match.objects.filter(tournament=tournament, winner__isnull=False).count() // 2

    # Check if the current round is the final round
    return rounds_played == num_rounds

from django.db.models import F

def generate_next_round(tournament, in_round):
    # Retrieve the winners of the current round
    round_matches = Match.objects.filter(tournament=tournament, in_round=in_round)
    winners = [match.winner for match in round_matches]

    rounds = in_round - 1  # change the round number for the next round

    # Create new matches for the next round
    new_matches = []
    for i in range(0, len(winners), 2):
        # Ensure there are at least two winners left to create a match
        if i + 1 < len(winners):
            match = Match.objects.create(
                tournament=tournament,
                player1=winners[i],
                player2=winners[i + 1],
                in_round=rounds
            )
            new_matches.append(match)

    return new_matches


def show_tournament_details(request:HttpRequest, tourment_id):
    tournament = Tournament.objects.get(id=tourment_id)
    matches = Match.objects.filter(tournament=tournament)
    comment = Comment.objects.filter(tournament=tournament)
    profile_user = Profile.objects.get(user=request.user)

    if request.method == "POST" and request.user.is_authenticated:
        new_comment = Comment(tournament=tournament, profile=profile_user, content=request.POST["content"])
        new_comment.save()
    match_len = matches.count()
    return render(request, 'tournament/tournament_details.html', {'tournament': tournament, 'matches': matches, "match_len":match_len, "comment":comment})


def show_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    matches = Match.objects.filter(tournament=tournament)
    match_len = matches.count()
    return render(request, 'tournament/tournaments_home.html', {'tournament': tournament, 'matches': matches, "match_len":match_len})



def enroll_view(request : HttpRequest,tourment_id):
    tourment=Tournament.objects.get(id=tourment_id)
    if tourment.number_of_players==0:
        return HttpResponse('Full')
    user_profile=Profile.objects.get(user=request.user)
    
    if user_profile.states=='2' :
        return HttpResponse("Not alloed to enroll")
    else :
        if TournamentPlayers.objects.filter(tourmnet=tourment,player=user_profile).exists():

            return HttpResponse("PLayers is enrolled ")
        else:
            user_inrolled_in=TournamentPlayers(tourmnet=tourment, player=user_profile) 
            tourment.number_of_players-=1
            tourment.save()
            user_inrolled_in.save()
            return HttpResponse("player enrolled ",tourment.number_of_players)
        

def announce_winner(request: HttpRequest, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)



    