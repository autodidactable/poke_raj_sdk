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
        self.BASE_URL = self.config.get("base_url", "https://pokeapi.co/api/v2")
        self.pokemon_id = self.config.get('pokemon', {}).get('id')
        self.pokemon_name = self.config.get('pokemon', {}).get('name')
        self.generation_id = self.config.get('generation', {}).get('id')
        self.generation_name = self.config.get('generation', {}).get('name')

    def fetch_pokemon(self):
        if self.pokemon_id:
            url = f"{self.BASE_URL}/pokemon/{self.pokemon_id}/"
            print(url)
        elif self.pokemon_name:
            url = f"{self.BASE_URL}/pokemon/{self.pokemon_name}/"
            print(url)
        else:
            print("Error: Either 'id' or 'name' is required for Pokémon in config.json.")
            return None

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return self.create_pokemon_from_api(data)
        except requests.exceptions.HTTPError as e:
            print(f"Error: Unable to fetch Pokémon - {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error: Network or API issue - {e}")

    def fetch_generation(self):
        if self.generation_id:
            url = f"{self.BASE_URL}/generation/{self.generation_id}/"
            print(url)
        elif self.generation_name:
            url = f"{self.BASE_URL}/generation/{self.generation_name}/"
            print(url)
        else:
            print("Error: Either 'id' or 'name' is required for Generation in config.json.")
            return None

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return self.create_generation_from_api(data)
        except requests.exceptions.HTTPError as e:
            print(f"Error: Unable to fetch Generation - {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error: Network or API issue - {e}")

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

    def create_generation_from_api(self, data):
        names = {name['language']['name']: name['name'] for name in data['names']}
        return Generation(
            id=data['id'],
            name=data['name'],
            names=names,
            main_region=data['main_region']['name']
        )

def print_pokemon(pokemon):
    if not pokemon:
        return
    print(f"ID: {pokemon.id}")
    print(f"Name: {pokemon.name.capitalize()}")
    print(f"Base Experience: {pokemon.base_experience}")
    print(f"Height: {pokemon.height}")
    print(f"Weight: {pokemon.weight}")
    print(f"Is Default: {'Yes' if pokemon.is_default else 'No'}")
    print(f"Order: {pokemon.order}")

    print("\nAbilities:")
    for ability in pokemon.abilities:
        print(f"- {ability.ability.name.capitalize()} (Hidden: {'Yes' if ability.is_hidden else 'No'})")

    print("\nMoves:")
    for move in pokemon.moves:
        print(f"- {move.move.name.capitalize()}")

    print("\nSprites:")
    print(f"Front Default: {pokemon.sprites.front_default}")
    print(f"Back Default: {pokemon.sprites.back_default}")

    print("\nLocation Area Encounters:")
    print(pokemon.location_area_encounters)

def print_generation(generation):
    if not generation:
        return
    print(f"ID: {generation.id}")
    print(f"Name: {generation.name.capitalize()}")
    print("Names in Different Languages:")
    for lang, name in generation.names.items():
        print(f"- {lang.capitalize()}: {name}")
    print(f"Main Region: {generation.main_region.capitalize()}")

if __name__ == "__main__":
    client = PokeAPIClient()

    try:
        pokemon = client.fetch_pokemon()
        if pokemon:
            print("Pokemon Details:")
            print_pokemon(pokemon)
    except Exception as e:
        print(f"Error fetching Pokémon data: {e}")

    try:
        generation = client.fetch_generation()
        if generation:
            print("\nGeneration Details:")
            print_generation(generation)
    except Exception as e:
        print(f"Error fetching Generation data: {e}")
