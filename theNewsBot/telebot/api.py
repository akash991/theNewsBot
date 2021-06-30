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

def lets_go(update, context):
    message = LETS_GO
    message += "\n\n"
    keys = helpers.get_data("news")
    for command in keys:
        message += "/{}\n".format(command)
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return "news"

def let_it_be(update, context):
    message = LET_IT_BE
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
        return_value = input_message.strip("/")
        for command in keys:
            message += "/{}\n".format(command)
        message += "\n/category\n"
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = message
        )
    elif isinstance(keys[0], dict):
        list_of_articles = keys
        for entry in keys[:10]:
            message += "[{}]({})\n\n".format(entry["title"], entry["link"])
        message += "\n/next\n/category"
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
            message += "You've reached the end of the news feed.\n"
            message += "/back\n/category\n"
        else:
            start_index = current_news_index
            stop_index = current_news_index + 10 
            for article in list_of_articles[start_index:stop_index]:
                message += "[{}]({})\n\n".format(article['title'], article['link'])
            message += "/next\n/back\n/category\n"
    if command == "/back":
        current_news_index -= 10
        if current_news_index < 10:
            start_index = 0
            stop_index = 10
            for article in list_of_articles[start_index:stop_index]:
                message += "[{}]({})\n\n".format(article['title'], article['link']) 
            message += "/next\n/category\n"
        else:
            start_index = current_news_index
            stop_index = current_news_index + 10
            for article in list_of_articles[start_index:stop_index]:
                message += "[{}]({})\n\n".format(article['title'], article['link'])        
            message += "/next\n/back\n/category\n"

    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message,
        disable_web_page_preview = True,
        parse_mode = "markdown"
    )
    return "previous_next"

def stop(update, context):
    message = "Thanks for your time. Have a great day"
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return "stop"
