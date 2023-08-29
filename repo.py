import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read("configs.ini")

class CookbookDbRepo: ## handles fetching of data from db into a list of dicts

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=config["DATABASE"]["host"],
            user=config["DATABASE"]["user"],
            password=config["DATABASE"]["password"],
            database=config["DATABASE"]["database"]
        )

    def getAllCuisines(self):
        mycursor = self.mydb.cursor()
        query = "select * from tianCookbookDatabase.cuisine;"
        mycursor.execute(query)
        resultSet = list(map(lambda result: dict(zip(mycursor.column_names, result)), mycursor.fetchall()))
        return resultSet

    def getDishesFromCuisine(self, cuisine):
        mycursor = self.mydb.cursor()
        query = f"select * from tianCookbookDatabase.dish where cuisine in (select cuisineId from tianCookbookDatabase.cuisine where cuisine = '{cuisine}')"
        mycursor.execute(query)
        results = list(map(lambda result: dict(zip(mycursor.column_names, result)), mycursor.fetchall()))
        return results

    def getDishFromName(self, dish):
        mycursor = self.mydb.cursor()
        query = f"select * from tianCookbookDatabase.dish where dish='{dish}'"
        mycursor.execute(query)
        result = dict(zip(mycursor.column_names, mycursor.fetchone())) 
        return result