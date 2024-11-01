class PokemonMove:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    @classmethod
    def from_json(cls, move_data):
        name = move_data["move"]["name"]
        url = move_data["move"]["url"]
        return cls(name, url)

    def __repr__(self):
        return f"PokemonMove(name={self.name}, url={self.url})"

#pokemon model
class Pokemon:
    def __init__(self, id, name, base_experience, height, weight, is_default, order, abilities, moves, sprites, location_area_encounters):
        self.id = id
        self.name = name
        self.base_experience = base_experience
        self.height = height
        self.weight = weight
        self.is_default = is_default
        self.order = order
        self.abilities = abilities  
        self.moves = moves          
        self.sprites = sprites      
        self.location_area_encounters = location_area_encounters

#generation model
class Generation:
    def __init__(self, id, name, names, main_region):
        self.id = id
        self.name = name
        self.names = names  
        self.main_region = main_region