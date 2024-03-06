import folium

from django.utils.timezone import localtime
from django.shortcuts import render, get_object_or_404

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.filter(
        appeared_at__lte=localtime(),
        disappeared_at__gte=localtime()
    ):
        if pokemon_entity.pokemon.image:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            img_url = request.build_absolute_uri(pokemon.image.url)
        else:
            img_url = None

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url':  img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id, img_url=None):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    if pokemon.image:
        img_url = request.build_absolute_uri(pokemon.image.url)

    pokemon_properties = {
        'pokemon_id': pokemon_id,
        'title_ru': pokemon.title,
        'img_url': img_url
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    if img_url:
        for pokemon_entity in PokemonEntity.objects.filter(
            pokemon=pokemon,
            appeared_at__lte=localtime(),
            disappeared_at__gte=localtime()
        ):
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                img_url
            )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_properties
    })
