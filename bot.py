import configparser
import telebot
import service
from telebot import types
import model

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
        generate_buttons_n_in_a_row(dishes, markUp, 3)
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
    infoArray = info.split("|")
    finalInformation = f"*{chosenInfo}*:\n"
    counter = 1
    for info in infoArray:
        if chosenInfo == "Instructions":
            finalInformation += str(counter) + ". " + info.strip() + "\n"
            counter += 1
        elif chosenInfo == "Ingredients":
            if info.strip()[-1] == ":":
                finalInformation += info.strip() + "\n"
            else:
                finalInformation += "- " + info.strip() + "\n"
        
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.send_message(message.chat.id, finalInformation, parse_mode="Markdown")
    prompt_final_actions(message, chosenDish)

def prompt_final_actions(message, chosenDish):
    text = f"Dish chosen: {chosenDish['dish']}\nWhat else would you like to do?"
    markUp = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=3)
    options = ["See Ingredients \U0001F966", "See Instructions \U0001F522", "Bye \U0001F44B", "Start over again"]
    markUp = generate_buttons_n_in_a_row(options, markUp, 2)
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


@bot.message_handler(commands=['add_dish'])
def start_add_dish(message):
    text = "What is the name of your new dish?"
    sentMessage = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sentMessage, handle_new_dish)

def handle_new_dish(message):
    dishName = message.text
    newDish = model.Dish(dish=dishName)
    text = f"Ok, your new dish name is *{dishName}*. Next, specify its cuisine type"
    cuisines = cookbookService.getCuisineNames()
    markUp = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    for cuisine in cuisines:
        markUp.add(types.KeyboardButton(cuisine))
    markUp.add("New Cuisine!")
    sentMessage = bot.send_message(message.chat.id, text, reply_markup=markUp, parse_mode="markdown")
    bot.register_next_step_handler(sentMessage, handle_cuisine_choice, newDish)

def handle_cuisine_choice(message, newDish):
    cuisine_choice = message.text
    if cuisine_choice == "New Cuisine!":
        text = "Sure, what will be your new cuisine type?"
        sentMessage = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(sentMessage, handle_new_cuisine, newDish)
    else:
        newDish.set_cuisine(cuisine_choice)
        text = f"Sure, *{newDish.get_name()}*'s cuisine type will be set as *{cuisine_choice}*"
        sentMessage = bot.send_message(message.chat.id, text, parse_mode="markdown")
        prompt_add_details(message, newDish=newDish, ingredients_or_instructions="ingredient")

def handle_new_cuisine(message, newDish):
    cuisine_name = message.text
    new_cuisine = model.Cuisine(cuisine_name)
    if cookbookService.saveCuisine(new_cuisine):
        text = f"New cuisine saved! Your new dish's cuisine type is set to *{cuisine_name}*"
        newDish.set_cuisine(cuisine_name)
        sentMessage = bot.send_message(message.chat.id, text, parse_mode="markdown")
        prompt_add_details(message, newDish=newDish, ingredients_or_instructions="ingredient")

def prompt_add_details(message, newDish, ingredients_or_instructions):
    text = f"Start adding {ingredients_or_instructions} for *{newDish.get_name()}*."
    sentMessage = bot.send_message(message.chat.id, text, parse_mode="markdown")
    bot.register_next_step_handler(sentMessage, handle_add_details, newDish, ingredients_or_instructions)

def handle_add_details(message, newDish, ingredients_or_instructions):
    reply = message.text
    if reply == "That's all.":
        theOther = "ingredient" if ingredients_or_instructions == "instruction" else "instruction"
        if len(newDish.ingredients) != 0 and len(newDish.instructions) != 0:
            text = f"Okay! Your {ingredients_or_instructions}s will be saved. Your dish is done and will now be saved."
            cookbookService.saveDish(newDish)
            sentMessage = bot.send_message(message.chat.id, text)
            message.text = newDish.dish
            choose_action_for_dish(message)
        else:
            text = f"Okay! Your {ingredients_or_instructions}s will be saved. Next add {theOther}s for this dish."
            sentMessage = bot.send_message(message.chat.id, text)
            prompt_add_details(message, newDish, theOther)
    else:
        if ingredients_or_instructions == "ingredient":
            newDish.add_ingredients(reply)
        elif ingredients_or_instructions == "instruction":
            newDish.add_instructions(reply)
        text = f"Okay, continue adding an {ingredients_or_instructions} and hit \"That's all\". when you are done!"
        markup = types.ReplyKeyboardMarkup()
        markup.add("That's all.")
        sentMessage = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(sentMessage, handle_add_details, newDish, ingredients_or_instructions)

#### Helper functions ####
def generate_buttons_n_in_a_row(options, markup, number_of_button_in_row):
    start = 0
    end = number_of_button_in_row
    while end <= len(options):
        markup.add(*options[start:end])
        start += number_of_button_in_row
        end += number_of_button_in_row
    
    markup.add(*options[start:])
    return markup


bot.infinity_polling()