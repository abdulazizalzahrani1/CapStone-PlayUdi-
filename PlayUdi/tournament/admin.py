from django.contrib import admin
from .models import Profile, Tournament,TournamentPlayers,Match
from comment.models import Comment
# Register your models here.


admin.site.register(Profile)
admin.site.register(Tournament)
admin.site.register(TournamentPlayers)
admin.site.register(Match)
admin.site.register(Comment)

