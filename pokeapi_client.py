import requests

class PokeAPIClient:
    BASE_URL = 'https://pokeapi.co/api/v2/'

    @staticmethod
    def get_pokemon(pokemon_id):
        """Fetch a Pokémon by its ID, returning its name, types, and abilities."""
        response = requests.get(f"{PokeAPIClient.BASE_URL}pokemon/{pokemon_id}/")
        if response.status_code == 200:
            data = response.json()
            return {
                'name': data.get('name', 'Unknown'),
                'id': pokemon_id,  # Directly use the provided pokemon_id
                'types': [t['type']['name'] for t in data.get('types', [])],
                'abilities': [a['ability']['name'] for a in data.get('abilities', [])]
            }
        else:
            print(f"Failed to retrieve Pokémon information for ID {pokemon_id}. Status Code: {response.status_code}")
            return None
