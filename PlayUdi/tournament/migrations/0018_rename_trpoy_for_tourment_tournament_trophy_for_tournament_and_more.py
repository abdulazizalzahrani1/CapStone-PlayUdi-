# Generated by Django 4.2.5 on 2023-09-10 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0017_profile_points_profile_user_rank_tournament_winner_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='trpoy_for_tourment',
            new_name='trophy_for_tournament',
        ),
        migrations.RenameField(
            model_name='tournamentplayers',
            old_name='tourmnet',
            new_name='tournament',
        ),
    ]
