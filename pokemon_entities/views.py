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


def get_pokemon_image(
        request,
        pokemon: Pokemon,
        default_image: str | tuple[str] = DEFAULT_IMAGE_URL
) -> str:
    if pokemon.image:
        img_url = request.build_absolute_uri(pokemon.image.url)
    else:
        img_url = request.build_absolute_uri(default_image)

    return img_url


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.filter(
        appeared_at__lte=localtime(),
        disappeared_at__gte=localtime()
    ):
        img_url = get_pokemon_image(request, pokemon_entity.pokemon)

        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        img_url = get_pokemon_image(request, pokemon)

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url':  img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    img_url = get_pokemon_image(request, pokemon)
    next_evolution = pokemon.next_evolution.first()

    pokemon_properties = {
        'pokemon_id': pokemon_id,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': img_url,
    }

    if pokemon.previous_evolution:
        pokemon_properties['previous_evolution'] = {
            'pokemon_id': pokemon.previous_evolution.id,
            'title_ru': pokemon.previous_evolution.title,
            'img_url': get_pokemon_image(request, pokemon.previous_evolution)
        }

    if next_evolution:
        pokemon_properties['next_evolution'] = {
            'pokemon_id': next_evolution.id,
            'title_ru': next_evolution.title,
            'img_url': get_pokemon_image(request, next_evolution)
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
