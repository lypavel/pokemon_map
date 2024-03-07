from django.db import models


class Pokemon(models.Model):
    title = models.CharField('Имя (на русском)', max_length=200)
    title_en = models.CharField(
        'Имя (на английском)',
        max_length=200,
        null=True
    )
    title_jp = models.CharField('Имя (на японском)', max_length=200, null=True)
    description = models.TextField('Описание', null=True, blank=True)
    image = models.ImageField(
        'Картинка',
        upload_to='pokemon_images',
        null=True,
        blank=True
    )
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name='next_evolutions',
        verbose_name='Из кого эволюционирует',
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Покемон',
        on_delete=models.CASCADE,
        related_name='entities'
    )
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField(
        'Дата появления'
    )
    disappeared_at = models.DateTimeField(
        'Дата исчезновения'
    )
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.pokemon.title} на {self.lat}, {self.lon}'
