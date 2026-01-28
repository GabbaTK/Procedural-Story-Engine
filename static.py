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

UPDATE_FILES = {"engine.py": "https://raw.githubusercontent.com/GabbaTK/Procedural-Story-Engine/refs/heads/main/engine.py", "builtin.json": "https://raw.githubusercontent.com/GabbaTK/Procedural-Story-Engine/refs/heads/main/builtin.json", "static.py": "https://raw.githubusercontent.com/GabbaTK/Procedural-Story-Engine/refs/heads/main/static.py"}
VERSION_URL = "https://raw.githubusercontent.com/GabbaTK/Procedural-Story-Engine/refs/heads/main/static.py"
VERSION_REGEX = r'VERSION = "\d+\.\d+.\d+"'
VERSION = "0.8.2"
CUSTOM_SCRIPT_WARNING = f"""{AnsiColorCodes.Red}
=============================

█░█░█ ▄▀█ █▀█ █▄░█ █ █▄░█ █▀▀
▀▄▀▄▀ █▀█ █▀▄ █░▀█ █ █░▀█ █▄█

=============================

This world has custom scripts!
Make sure you trust the author of those scripts as they could do damage to your system!

Do you want to continue? (y/n) {AnsiColorCodes.Reset}"""

PADDING_CHAR = "═"
SPLASH_SCREEN = f"""{AnsiColorCodes.Cyan}
╔══════════════════════════[[PADDING]]═════════╗
║     PROCEDURAL STORY ENGINE v[[ENGINE_VERSION]]     ║
╚══════════════════════════[[PADDING]]═════════╝

  World: [[WORLD_NAME]]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Available Commands:

Movement: w/a/s/d
Actions:  [[ACTIONS]]

If you mistype an action, press enter. Backspace doesn't work.
Progress is automatically saved when you exit.
To manually save, press SPACE, then type 'save'.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{AnsiColorCodes.Reset}"""
YOU_DIED = f"""{AnsiColorCodes.Red}
╔══════════════════╗
║     YOU DIED     ║
╚══════════════════╝

Level: [[LEVEL]]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Better luck next time!
{AnsiColorCodes.Reset}"""

# --------------------------------------
# CONFIG
# --------------------------------------
MIN_TERM_WIDTH = 50 # Random value
ENTITIES = ["chest", "spawn_point"] # Required for "findEntityFromTemplate"
USER_BASIC_MOVEMENT = ["w", "a", "s", "d"] # Movement
USER_ADVANCED_MOVEMENT = ["inspect", "open", "close", "lock", "unlock", "gather", "leave", "pickup"] # Actions for entities
USER_STATIC_ACTION = ["inventory", "quit", "save"] # Actions to do anywhere
BLOCKING_TILES = ["-", "|", "+", "~", "\\", "/"]
ETC_MAP = dotdict({ # Entity to char map
    "player": "@",
    "spawn_point": "S",
    "chest": "=",
    "exit": "E",
    "item": "*"
})
#    "player": "@",   # standard
#    "npc": "&",      # humanoid / intelligent entity
#    "chest": "=",    # container / storage
#    "door": "+",     # classic closed door
#    "item": "*",     # generic pickup
#    "object": "#",   # solid / blocking object
#    "mechanism": "%",# traps, levers, machinery
#    "spawn": "!",    # point of interest / danger