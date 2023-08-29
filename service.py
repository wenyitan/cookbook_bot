import repo

class CookbookService:

    def __init__(self):
        self.cookbook = repo.CookbookDbRepo()

    def getCuisineNames(self):
        cuisines = self.cookbook.getAllCuisines()
        return [cuisine["cuisine"] for cuisine in cuisines]
    
    def getDishNamesFromCuisine(self, chosenCuisine):
        dishes = self.cookbook.getDishesFromCuisine(chosenCuisine)
        return [dish["dish"] for dish in dishes]
    
    def getDishByName(self, chosenDish):
        dish = self.cookbook.getDishFromName(chosenDish)
        return dish