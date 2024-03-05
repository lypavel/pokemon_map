from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='pokemon_photos',
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
