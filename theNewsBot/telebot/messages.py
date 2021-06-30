from enum import Enum

START_MESSAGE = "Hello!! I'm SAMA4, your personal news assistant.\nI hope you are having a great day but let's make it even better.\n/lets_go\n/let_it_be"
LET_IT_BE = "Seriously!!\nThen why waste my time, 'bot' kaam hai ;)"
LETS_GO = "Let's begin then, please select from one of the following categories."

class State(Enum):
    START = 0
    STOP = -1
    LEVEL1 = 1
    LEVEL2 = 2