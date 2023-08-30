import repo

class CookbookService:

    def __init__(self):
        self.cookbookRepo = repo.CookbookDbRepo()

    def getCuisineNames(self):
        cuisines = self.cookbookRepo.getAllCuisines()
        return [cuisine["cuisine"] for cuisine in cuisines]
    
    def getDishNamesFromCuisine(self, chosenCuisine):
        dishes = self.cookbookRepo.getDishesFromCuisine(chosenCuisine)
        return [dish["dish"] for dish in dishes]
    
    def getDishByName(self, chosenDish):
        dish = self.cookbookRepo.getDishFromName(chosenDish)
        return dish
    
    def saveCuisine(self, newCuisine):
        return self.cookbookRepo.saveNewCuisine(newCuisine)
    
    def saveDish(self, newDish):
        return self.cookbookRepo.saveNewDish(newDish)