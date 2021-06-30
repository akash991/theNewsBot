import api
from telegram import Bot
from messages import State
from credentials import TOKEN
from telegram.ext import CommandHandler, ConversationHandler, Updater
from theHindu.helpers import get_all_keys

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

states = {}
for key, val in get_all_keys().items():
    states[key] = []
    if len(val) > 1:
        for entry in val:
            states[key].append(CommandHandler(
                command=entry,
                callback=api.get_data
            ))
        states[key].append(
            CommandHandler(
                command="category",
                callback=api.lets_go
            )
        )
    else:
        states[key] = [
            CommandHandler(
                command="next",
                callback=api.get_previous_next
            ),
            CommandHandler(
                command="back",
                callback=api.get_previous_next
            )
        ]

start_end = {
    "start": [
        CommandHandler(
            command="lets_go",
            callback=api.lets_go
        ),
        CommandHandler(
            command="let_it_be",
            callback=api.let_it_be
        )
    ],
    "stop": [
        CommandHandler(
            command="stop",
            callback=api.stop
        )
    ],
    "previous_next": [
        CommandHandler(
            command="back",
            callback=api.get_previous_next
            ),
        CommandHandler(
            command="next",
            callback=api.get_previous_next
            ),
        CommandHandler(
            command="category",
            callback=api.lets_go
            )
        ]
    }

conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler(
            command="start",
            callback=api.start
        )
    ],
    states={**states, **start_end},
    fallbacks=[
        CommandHandler(
            command="stop",
            callback=ConversationHandler.END
        )
    ],
    allow_reentry=True
)

dispatcher.add_handler(conversation_handler)
updater.start_polling()
