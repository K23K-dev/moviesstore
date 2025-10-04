from django.contrib import admin
from .models import Movie, Review, Petition, PetitionVote

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class PetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'proposer', 'created_at', 'votes_count')
    search_fields = ('title', 'proposer_username')
class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ('petition', 'user', 'created_at')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Petition, PetitionAdmin)
admin.site.register(PetitionVote, PetitionVoteAdmin)