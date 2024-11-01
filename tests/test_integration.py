import unittest
import requests
from unittest.mock import patch
from poke_raj_sdk.client import PokeAPIClient
from poke_raj_sdk.models import Pokemon, Generation

class TestPokeAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = PokeAPIClient()

    @patch('poke_raj_sdk.client.requests.get')
    def test_fetch_pokemon(self, mock_get):
        mock_response = {
            'id': 1,
            'name': 'bulbasaur',
            'base_experience': 64,
            'height': 7,
            'weight': 69,
            'is_default': True,
            'order': 1,
            'abilities': [{'ability': {'name': 'overgrow'}, 'is_hidden': False}],
            'moves': [{'move': {'name': 'tackle'}}],
            'sprites': {'front_default': 'front_sprite_url', 'back_default': 'back_sprite_url'},
            'location_area_encounters': 'some_location_area'
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        pokemon = self.client.fetch_pokemon(1)
        self.assertIsInstance(pokemon, Pokemon)
        self.assertEqual(pokemon.id, 1)

    @patch('poke_raj_sdk.client.requests.get')
    def test_fetch_generation(self, mock_get):
        mock_response = {
            'id': 1,
            'name': 'generation-i',
            'names': [{'language': {'name': 'en'}, 'name': 'Generation I'}],
            'main_region': {'name': 'kanto'}
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        generation = self.client.fetch_generation(1)
        self.assertIsInstance(generation, Generation)
        self.assertEqual(generation.id, 1)

    @patch('poke_raj_sdk.client.requests.get')
    def test_fetch_pokemon_not_found(self, mock_get):
        # Mock a 404 response and raise an HTTPError
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.fetch_pokemon(9999)  # Assuming 9999 is an invalid ID

    @patch('poke_raj_sdk.client.requests.get')
    def test_fetch_generation_not_found(self, mock_get):
        # Mock a 404 response and raise an HTTPError
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.fetch_generation(9999)  # Assuming 9999 is an invalid ID

if __name__ == '__main__':
    unittest.main()
