from messages import *
from theNewsBot.telebot import rssfeeds

list_of_articles = []
current_news_index = 0
news_source = None

def start(update, context):
    """
    Gets trigerred when user types in /start
    """
    message = START_MESSAGE
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return "start"

def select_sources(update, context):
    """
    Gets trigerred when the user types in /yes after
    starting the conversation
    """
    global news_source 
    news_source = None
    message = SELECT_SOURCE
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return "source"

def the_Hindu(update, context):
    """
    """
    global news_source
    news_source = "theHindu"
    message = BEGIN
    keys = rssfeeds.get_data(news_source)
    for command in keys:
        message += "/{}\n".format(command)
    message += SOURCE
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return news_source

def the_ET(update, context):
    """
    """
    global news_source
    news_source = "theET"
    message = BEGIN
    keys = rssfeeds.get_data(news_source)
    for command in keys:
        message += "/{}\n".format(command)
    message += SOURCE
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return news_source


def begin(update, context):
    """
    Gets trigerred when user types in /yes after
    starting the conversation.
    """
    message = BEGIN
    keys = rssfeeds.get_data(news_source)
    for command in keys:
        message += "/{}\n".format(command)
    message += SOURCE
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return news_source

def get_data(update, context):
    """
    Gets trigerred when user selects one of the
    categories/rssfeed
    """
    global list_of_articles
    message = ""
    input_message = update.message.text
    keys = rssfeeds.get_data(input_message.strip("/"))
    if isinstance(keys[0], str):
        # If the return type is a list of strings, means that there are suboptions
        message = SUBCATEGORIES_BEGIN
        for command in keys:
            message += "/{}\n".format(command)
        message += CATEGORY
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = message
        )
    elif isinstance(keys[0], dict):
        # If the return type is a list of dictionary, means that its an rss feed
        # and has several news articles in the form of a dictionary.
        count = 1
        list_of_articles = keys
        for entry in keys[:10]:
            message += "[{}. {}]({})\n\n".format(count, entry["title"], entry["link"])
            count += 1
        message += NEXT_CATEGORY_SOURCE
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = message,
            disable_web_page_preview = True,
            parse_mode = "markdown"
        )
    return input_message.strip("/")

def get_next(update, context):
    """
    Gets trigerred when user selects /next.
    Navigates to the next set of news under the same category
    """
    message = ""
    global current_news_index
    current_news_index += 10
    
    if current_news_index >= len(list_of_articles):
        message += THATS_IT
        message += BACK_CATEGORY_SOURCE
    else:
        start_index = current_news_index
        stop_index = current_news_index + 10 
        count = start_index + 1
        for article in list_of_articles[start_index:stop_index]:
            message += "[{}. {}]({})\n\n".format(count, article['title'], article['link'])
            count += 1
        message += NEXT_BACK_CATEGORY_SOURCE

    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message,
        disable_web_page_preview = True,
        parse_mode = "markdown"
    )
    return "next"

def get_back(update, context):
    """
    Gets trigerred when user selects /back
    while scroling through the list of articles.
    """
    message = ""
    global current_news_index
    current_news_index -= 10

    if current_news_index < 10:
        start_index = 0
        stop_index = 10
        count = 1
    else:
        start_index = current_news_index
        stop_index = current_news_index + 10
        count = start_index
        
    for article in list_of_articles[start_index:stop_index]:
        message += "[{}. {}]({})\n\n".format(count, article['title'], article['link']) 
        count += 1

    if current_news_index < 10:
        message += NEXT_CATEGORY_SOURCE
    else:    
        message += NEXT_BACK_CATEGORY_SOURCE
    
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message,
        disable_web_page_preview = True,
        parse_mode = "markdown"
    )
    return "back"

def stop(update, context):
    """
    Gets trigerred when user types in /stop
    """
    message = STOP_MESSAGE
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = message
    )
    return "stop"
