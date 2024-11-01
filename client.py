import os
import requests
import json
from .models import Pokemon, Generation

class Ability:
    def __init__(self, name, is_hidden):
        self.ability = AbilityDetail(name)
        self.is_hidden = is_hidden

class AbilityDetail:
    def __init__(self, name):
        self.name = name

class Move:
    def __init__(self, name):
        self.move = MoveDetail(name)

class MoveDetail:
    def __init__(self, name):
        self.name = name

class Sprite:
    def __init__(self, front_default, back_default):
        self.front_default = front_default
        self.back_default = back_default

class PokeAPIClient:
    def __init__(self):
        # Get the directory of the current file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, 'config.json')

        # Load the configuration
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)

        # Set the base URL and other parameters from the config
        self.BASE_URL = self.config['base_url']
        self.pokemon_id = self.config['pokemon']['id']
        self.pokemon_name = self.config['pokemon']['name']
        self.generation_id = self.config['generation']['id']
        self.generation_name = self.config['generation'].get('name', None)  # Optional

    def fetch_pokemon(self, pokemon_id):
        url = f"{self.BASE_URL}/pokemon/{pokemon_id}/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return self.create_pokemon_from_api(data)

    def create_pokemon_from_api(self, data):
        abilities = [Ability(ability['ability']['name'], ability['is_hidden']) for ability in data['abilities']]
        moves = [Move(move['move']['name']) for move in data['moves']]
        sprites = Sprite(data['sprites']['front_default'], data['sprites']['back_default'])

        return Pokemon(
            id=data['id'],
            name=data['name'],
            base_experience=data['base_experience'],
            height=data['height'],
            weight=data['weight'],
            is_default=data['is_default'],
            order=data['order'],
            abilities=abilities,
            moves=moves,
            sprites=sprites,
            location_area_encounters=data['location_area_encounters']
        )

    def fetch_generation(self, generation_id):
        url = f"{self.BASE_URL}/generation/{generation_id}/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return self.create_generation_from_api(data)

    def create_generation_from_api(self, data):
        names = {name['language']['name']: name['name'] for name in data['names']}
        return Generation(
            id=data['id'],
            name=data['name'],
            names=names,
            main_region=data['main_region']['name']
        )

def print_pokemon(pokemon):
    print(f"ID: {pokemon.id}")
    print(f"Name: {pokemon.name.capitalize()}")
    print(f"Base Experience: {pokemon.base_experience}")
    print(f"Height: {pokemon.height}")
    print(f"Weight: {pokemon.weight}")
    print(f"Is Default: {'Yes' if pokemon.is_default else 'No'}")
    print(f"Order: {pokemon.order}")

    # Print abilities
    print("\nAbilities:")
    for ability in pokemon.abilities:
        print(f"- {ability.ability.name.capitalize()} (Hidden: {'Yes' if ability.is_hidden else 'No'})")

    # Print moves
    print("\nMoves:")
    for move in pokemon.moves:
        print(f"- {move.move.name.capitalize()}")

    # Print sprites
    print("\nSprites:")
    print(f"Front Default: {pokemon.sprites.front_default}")
    print(f"Back Default: {pokemon.sprites.back_default}")

    # Print location area encounters
    print("\nLocation Area Encounters:")
    print(pokemon.location_area_encounters)

def print_generation(generation):
    print(f"ID: {generation.id}")
    print(f"Name: {generation.name.capitalize()}")
    print("Names in Different Languages:")
    for lang, name in generation.names.items():
        print(f"- {lang.capitalize()}: {name}")
    print(f"Main Region: {generation.main_region.capitalize()}")

if __name__ == "__main__":
    client = PokeAPIClient()

    # Example: Fetching the Pokémon specified in the config
    try:
        pokemon = client.fetch_pokemon(client.pokemon_id)
        print("Pokemon Details:")
        print_pokemon(pokemon)
    except Exception as e:
        print(f"Error fetching Pokémon data: {e}")

    # Example: Fetching the generation specified in the config
    try:
        generation = client.fetch_generation(client.generation_id)
        print("\nGeneration Details:")
        print_generation(generation)
    except Exception as e:
        print(f"Error fetching Generation data: {e}")
