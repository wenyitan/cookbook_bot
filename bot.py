import configparser
import telebot
import service
from telebot import types

config = configparser.ConfigParser()
config.read("configs.ini")
BOT_TOKEN = config["TELEGRAM"]["token"]

bot = telebot.TeleBot(BOT_TOKEN)
cookbookService = service.CookbookService()

chosenDishUniversal = None

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Send /cuisine to start!")
    bot.send_message(message.chat.id, "For the best user experience, strictly stick to choosing from the options given.")


@bot.message_handler(commands=['cuisine'])
def get_cuisines(message):
    cuisines = cookbookService.getCuisineNames()
    markUp = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    for cuisine in cuisines:
        markUp.add(types.KeyboardButton(cuisine))
    sentMessage = bot.send_message(message.chat.id, "Choose a cuisine!", reply_markup=markUp)
    bot.register_next_step_handler(sentMessage, get_dishes_from_cuisine, cuisines)

def get_dishes_from_cuisine(message, cuisines):
    chosenCuisine = message.text
    if chosenCuisine not in cuisines:
        text = "Please choose a cuisine from the list!"
        sentMessage = bot.send_message(message.chat.id, text)
        get_cuisines(message)

    else :
        text = f"Which of the following *{chosenCuisine}* dishes do you want?"
        dishes = cookbookService.getDishNamesFromCuisine(chosenCuisine)
        markUp = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for dish in dishes:
            markUp.add(types.KeyboardButton(dish))
        sentMessage = bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markUp)
        bot.register_next_step_handler(sentMessage, choose_action_for_dish)
        
def choose_action_for_dish(message):
    chosenDish = message.text

    text = f"You have chosen *{chosenDish}*. What would you like to see?"
    chosenDish = cookbookService.getDishByName(chosenDish)
    markUp = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = ["Ingredients \U0001F966", "Instructions \U0001F522"]
    for option in options:
        markUp.add(types.KeyboardButton(option))
    
    sentMessage = bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markUp)
    bot.register_next_step_handler(sentMessage, show_information_for_dish, chosenDish)

def show_information_for_dish(message, chosenDish):
    chosenInfo = message.text.replace("See ", "").split(" ")[0]
    text = f"Here are the {chosenInfo} for {chosenDish['dish']}:"
    info = chosenDish[chosenInfo.lower()]
    infoArray = info.split(",")
    finalInformation = f"*{chosenInfo}*:\n"
    for info in infoArray:
        finalInformation += info.strip() + "\n"
        
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.send_message(message.chat.id, finalInformation, parse_mode="Markdown")
    prompt_final_actions(message, chosenDish)

def prompt_final_actions(message, chosenDish):
    text = f"Dish chosen: {chosenDish['dish']}\nWhat else would you like to do?"
    markUp = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=3)
    options = ["See Ingredients \U0001F966", "See Instructions \U0001F522", "Bye \U0001F44B", "Start over again"]
    for option in options:
        markUp.add(types.KeyboardButton(option))
    sentMessage = bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markUp)
    bot.register_next_step_handler(sentMessage, handle_final_action, chosenDish)

def handle_final_action(message, chosenDish):
    chosenAction = message.text
    if chosenAction.split(" ", 1)[0] == "See":
        show_information_for_dish(message, chosenDish)
    elif chosenAction == "Start over again":
        get_cuisines(message)
    else:
        markUp = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Bye!!! \U0001F44B", parse_mode="Markdown", reply_markup=markUp)


bot.infinity_polling()