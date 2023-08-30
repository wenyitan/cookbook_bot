class Dish:
    def __init__(self, dish):
        self.dish = dish
        self.ingredients = []
        self.instructions = []
        self.cuisine = None

    def add_ingredients(self, ingredient):
        self.ingredients.append(ingredient)
    
    def add_instructions(self, instruction):
        self.instructions.append(instruction)

    def set_cuisine(self, cuisine):
        self.cuisine = cuisine

    def get_cuisine(self):
        return self.cuisine

    def get_name(self):
        return self.dish
    
    def get_instructions(self):
        return "|".join(self.instructions)
    
    def get_ingredients(self):
        return "|".join(self.ingredients)

class Cuisine:
    def __init__(self, cuisine):
        self.cuisine = cuisine

    def getName(self):
        return self.cuisine
