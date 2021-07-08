import os
import api
import rssfeeds
from telegram import Bot
from telegram.ext import Updater, CommandHandler, ConversationHandler

def generate_conversation_handler_states_on_rssfeeds(handler_states):
    """
    Generate conv handler states based on the feeds from different sources
    """
    rss_feeds = rssfeeds.get_all_keys()
    for k, v in rss_feeds.items():
        handler_states[k] = []
        if isinstance(v, list):
            # If there are suboptions available for the given feed.
            # Create a CommandHandler for each option.
            for entry in v:
                handler_states[k].append(CommandHandler(command=entry, callback=api.get_data))
        if isinstance(v, str):
            # If there are no suboption and only contains the url to the rssfeed
            # Add CommandHandler to navigate between different articles in a given category
            handler_states[k] = [
                CommandHandler(command="next", callback=api.get_next),
                CommandHandler(command="back", callback=api.get_back)
            ]
        # Add category CommandHandler, this will help to navigate back to the list of categories
        handler_states[k].append(CommandHandler(command="category",callback=api.begin))
        handler_states[k].append(CommandHandler(command="source",callback=api.select_sources))
    return handler_states

def generate_conversation_handler_states():
    """
    Function to create different states in the ConversationHandler

    Parameters:
        None
    
    Return:
        dict: representing the handler states
    """
    handler_states = {}

    # CommandHandler to recognize the start of conversation
    handler_states["start"] = [CommandHandler(command="yes", callback=api.select_sources)]
    # CommandHandler to stop the conversation
    handler_states["stop"] = [CommandHandler(command="stop", callback=api.stop)]

    # CommandHandler to navigate forward/backward while going through the articles.
    for state in ["next", "back"]:
        handler_states[state] = [
            CommandHandler(command="next", callback=api.get_next),
            CommandHandler(command="back", callback=api.get_back),
            CommandHandler(command="category", callback=api.begin),
            CommandHandler(command="source", callback=api.select_sources)
        ]
    handler_states["source"] = []
    sources = ["theHindu", "theEconomicTimes", "theTimesOfIndia", "theEconomist"]
    for source in sources:
        handler_states["source"].append(CommandHandler(command=source, callback=api.get_rss_feeds))
    handler_states = generate_conversation_handler_states_on_rssfeeds(handler_states)
    return handler_states

# Creating the ConversationHandler object
# Entry point is /start
# Gets the different states based on the RSS Feed structure
# CommandHandler to handle during failures/error
conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler(
            command="start",
            callback=api.start
        )
    ],
    states = generate_conversation_handler_states(),
    fallbacks=[
        CommandHandler(
            command="stop",
            callback=ConversationHandler.END
        )
    ],
    allow_reentry=True
)

token = os.getenv("TOKEN")
bot = Bot(token=token)
updater = Updater(token=token)
dispatcher = updater.dispatcher

# Add conversation handler to the dispatcher
dispatcher.add_handler(conversation_handler)
# Start polling
updater.start_polling()
