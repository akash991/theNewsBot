from messages import *
from theHindu import helpers

list_of_articles = []
current_news_index = 0

def start(update, context):
    message = START_MESSAGE
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return "start"

def begin(update, context):
    message = QUENCH_IT
    keys = helpers.get_data("news")
    for command in keys:
        message += "/{}\n".format(command)
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return "news"

def noBegin(update, context):
    message = NO_THANKS
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return "stop"

def get_data(update, context):
    global list_of_articles
    message = ""
    return_value = "previous_next"
    input_message = update.message.text
    keys = helpers.get_data(input_message.strip("/"))
    if isinstance(keys[0], str):
        message = SUBCATEGORIES_BEGIN
        return_value = input_message.strip("/")
        for command in keys:
            message += "/{}\n".format(command)
        message += CATEGORY
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = message
        )
    elif isinstance(keys[0], dict):
        count = 1
        list_of_articles = keys
        for entry in keys[:10]:
            message += "[{}. {}]({})\n\n".format(count, entry["title"], entry["link"])
            count += 1
        message += NEXT_CATEGORY
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = message,
            disable_web_page_preview = True,
            parse_mode = "markdown"
        )
    return return_value

def get_previous_next(update, context):
    message = ""
    command = update.message.text
    global current_news_index
    if command == "/next":
        current_news_index += 10
        if current_news_index >= len(list_of_articles):
            message += THATS_IT
            message += BACK_CATEGORY
        else:
            start_index = current_news_index
            stop_index = current_news_index + 10 
            count = start_index + 1
            for article in list_of_articles[start_index:stop_index]:
                message += "[{}. {}]({})\n\n".format(count, article['title'], article['link'])
                count += 1
            message += NEXT_BACK_CATEGORY
    if command == "/back":
        current_news_index -= 10
        if current_news_index < 10:
            start_index = 0
            stop_index = 10
            count = 1
            for article in list_of_articles[start_index:stop_index]:
                message += "[{}. {}]({})\n\n".format(count, article['title'], article['link']) 
                count += 1
            message += NEXT_CATEGORY
        else:
            start_index = current_news_index
            stop_index = current_news_index + 10
            count = start_index
            for article in list_of_articles[start_index:stop_index]:
                message += "[{}. {}]({})\n\n".format(article['title'], article['link'])  
                count += 1      
            message += NEXT_BACK_CATEGORY

    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message,
        disable_web_page_preview = True,
        parse_mode = "markdown"
    )
    return "previous_next"

def stop(update, context):
    message = STOP_MESSAGE
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return "stop"
