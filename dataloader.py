import mysql.connector
import configparser
import pandas as pd
import json

config = configparser.ConfigParser()
config.read("configs.ini")


mydb = mysql.connector.connect(
    host=config["DATABASE"]["host"],
    user=config["DATABASE"]["user"],
    password=config["DATABASE"]["password"],
    database=config["DATABASE"]["database"]
)

mycursor = mydb.cursor()

# mycursor.execute("Create DATABASE tianCookbookDatabase")

## Cuisine table to allocate japanese, korean etc.
# mycursor.execute("CREATE TABLE cuisine (cuisine VARCHAR(255))")
# mycursor.execute("ALTER TABLE tianCookbookDatabase.dish RENAME COLUMN ingrendients TO ingredients;")

# sql = "INSERT INTO cuisine (cuisine) VALUES (%s)"
# val = [
#   ('Japanese',), ('Korean',)
# ]

# mycursor.executemany(sql, val)

# mydb.commit()

## Dish table
# mycursor.execute("CREATE TABLE dish (dishId INT AUTO_INCREMENT PRIMARY KEY, dish VARCHAR(255), ingrendients LONGTEXT, instructions LONGTEXT, cuisine INT)")

# df = pd.read_csv('Cookbook.csv')
# df = list(map(lambda x: tuple(x), df.values))

# query = "INSERT INTO `tianCookbookDatabase`.`dish` (`dish`, `ingredients`, `instructions`, `cuisine`) VALUES (%s, %s, %s, %s);"
# mycursor.executemany(query, df)

# mydb.commit()