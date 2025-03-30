from django.contrib import admin

# Register your models here.
from .models import Developer, Publiher, Genre, Game, Transaction, Cart, Image,MinSystemRequirements,RecommendedSystemRequirements

admin.site.register(Developer)
admin.site.register(Publiher)
admin.site.register(Genre)
admin.site.register(Game)
admin.site.register(Transaction)
admin.site.register(Cart)
admin.site.register(Image)
admin.site.register(MinSystemRequirements)
admin.site.register(RecommendedSystemRequirements)