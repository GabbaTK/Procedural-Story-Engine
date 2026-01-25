import os

# --------------------------------------
# GENERAL
# --------------------------------------
if os.name == "nt":
    import msvcrt
    getchfunc = msvcrt.getch
    getch = lambda: getchfunc().decode("ASCII")
elif os.name == "posix":
    import getch as getchlib
    getch = getchlib.getch
else: raise Exception("Unsuported OS")

def toDotdict(obj):
    if isinstance(obj, dict):
        return dotdict({k: toDotdict(v) for k, v in obj.items()})
    elif isinstance(obj, list):
        return [toDotdict(item) for item in obj]
    else:
        return obj

class AnsiColorCodes:
    Reset = "\033[0m"
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    White = "\033[37m"

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

CUSTOM_SCRIPT_WARNING = f"""{AnsiColorCodes.Red}
=============================

█░█░█ ▄▀█ █▀█ █▄░█ █ █▄░█ █▀▀
▀▄▀▄▀ █▀█ █▀▄ █░▀█ █ █░▀█ █▄█

=============================

This world has custom scripts!
Make sure you trust the author of those scripts as they could do damage to your system!

Do you want to continue? (y/n) {AnsiColorCodes.Reset}"""

# --------------------------------------
# CONFIG
# --------------------------------------
MIN_TERM_WIDTH = 50 # Random value
ENTITIES = ["chest", "spawn_point"] # Required for "findEntityFromTemplate"
USER_BASIC_MOVEMENT = ["w", "a", "s", "d"] # Movement
USER_ADVANCED_MOVEMENT = ["inspect", "open", "close", "lock", "unlock", "gather"] # Actions for entities
USER_STATIC_ACTION = ["inventory", "quit"] # Actions to do anywhere
ETC_MAP = dotdict({ # Entity to char map
    "player": "@",
    "spawn_point": "S",
    "chest": "="
})
#    "player": "@",   # standard
#    "npc": "&",      # humanoid / intelligent entity
#    "chest": "=",    # container / storage
#    "door": "+",     # classic closed door
#    "item": "*",     # generic pickup
#    "object": "#",   # solid / blocking object
#    "mechanism": "%",# traps, levers, machinery
#    "spawn": "!",    # point of interest / danger