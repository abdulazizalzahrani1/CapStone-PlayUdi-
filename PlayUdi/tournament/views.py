from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Player, Tournament, Match
import random
import math
# Create your views here.

def tournament_view(request: HttpRequest):
    return render(request, 'tournament/tournaments_home.html')


def create_tournament(request):
    if request.method == 'POST':
        # Get the number of players from the form
        num_players = int(request.POST['num_players'])

        # Create a new tournament
        tournament = Tournament.objects.create(name="My Tournament")

        # Create players and matches for the first round
        players = []
        for i in range(num_players):
            player = Player.objects.create(name=f"Player {i + 1}")
            players.append(player)

        # Randomly assign players to matches for the first round
        rounds = math.log2(num_players)
        random.shuffle(players)
        matches = []
        for i in range(0, num_players, 2):
            match = Match.objects.create(tournament=tournament, player1=players[i], player2=players[i + 1], in_round=rounds)
            matches.append(match)

        return render(request, 'tournament/tournaments_home.html', {'tournament': tournament, 'matches': matches})

    return render(request, 'tournament/create_tournament.html')

def select_winner(request, match_id):

    match = Match.objects.get(id=match_id)

    if request.method == 'POST':
        winner_id = int(request.POST['winner'])
        winner = Player.objects.get(id=winner_id)

        # Update the match with the winner
        match.winner = winner
        match.save()

        # Check if all matches in the round have winners
        tournament = match.tournament
        round_matches = Match.objects.filter(tournament=tournament, winner=None)
        

        if not round_matches and match.in_round > 1:
                
            # Generate the next round if all matches have winners
            # if is_final_round(tournament):
                # return redirect('tournament:show_tournament', tournament_id=match.tournament.id)
            match.in_round = match.in_round -1 
            if match.in_round >= 1:
                generate_next_round(tournament)
                # matchs = Match.objects.all()
                # for match in matchs:
                #     match.winner = None
                #     match.save()

            
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

def generate_next_round(tournament):
    # Retrieve the winners of the current round
    round_matches = Match.objects.filter(tournament=tournament)
    # for match in round_matches:
    #     if match.in_round 
    winners = [match.winner for match in round_matches]

    rounds = round_matches.first().in_round - 1
    # Create new matches for the next round
    new_matches = []
    for i in range(0, len(winners) - 1, 2):
        match = Match.objects.create(tournament=tournament, player1=winners[i], player2=winners[i + 1], in_round= rounds)
        new_matches.append(match)

def show_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    matches = Match.objects.filter(tournament=tournament)
    match_len = matches.count()
    return render(request, 'tournament/tournaments_home.html', {'tournament': tournament, 'matches': matches, "match_len":match_len})
