import yaml
import os
from static import *
from copy import deepcopy as dc
import io
import time
import contextlib
import json

# --------------------------------------
# EXCEPTIONS
# --------------------------------------
class WorldNotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class WorldAlreadyLoadedException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class RoomNotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class EntityNotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class HandlerNotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class InvalidTemplateException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class ItemNotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

# --------------------------------------
# MAIN
# --------------------------------------
class Player:
    def __init__(self):
        self.coords = [None, None]
        self.hp = 20
        self.max_hp = 20
        self.level = 1
        self.inventory = [toDotdict({
    "id": "key",
    "name": "Key",
    "uid": None,
    "lock_id": "asdf"
})]
        self.engine = None

    def reset(self):
        """Fully resets the player"""

        self.coords = [None, None]
        self.hp = 20
        self.max_hp = 20
        self.level = 1
        self.inventory = []

    def moveUp(self) -> bool:
        """Move the player. Returns True if moved, otherwise False"""

        tile = self.engine.current_room.layout.strip().split("\n")[self.coords[0]][self.coords[1] - 1]

        if tile != "-" and tile != "|" and tile != "+":
            self.coords[1] -= 1
            return True
        
        return False
    
    def moveDown(self) -> bool:
        """Move the player. Returns True if moved, otherwise False"""

        tile = self.engine.current_room.layout.strip().split("\n")[self.coords[0]][self.coords[1] + 1]

        if tile != "-" and tile != "|" and tile != "+":
            self.coords[1] += 1
            return True
        
        return False

    def moveLeft(self) -> bool:
        """Move the player. Returns True if moved, otherwise False"""

        tile = self.engine.current_room.layout.strip().split("\n")[self.coords[0] - 1][self.coords[1]]

        if tile != "-" and tile != "|" and tile != "+":
            self.coords[0] -= 1
            return True
        
        return False

    def moveRight(self) -> bool:
        """Move the player. Returns True if moved, otherwise False"""

        tile = self.engine.current_room.layout.strip().split("\n")[self.coords[0] + 1][self.coords[1]]

        if tile != "-" and tile != "|" and tile != "+":
            self.coords[0] += 1
            return True
        
        return False

    def doAction(self, action: str):
        """Do an action

        Args:
            action (str): The action to do.

        Raises:
            ActionNotFoundException: That action does not exit
        """

        current_entity = self.engine.findEntityByCoords(self.engine.current_room, self.coords)

        if self.__staticAction(action): return

        if not current_entity: return
        if action not in current_entity.get("actions", {}): return

        handler = current_entity.actions[action]
        namespace, func = self.engine._handlerExists(handler, action)

        func = list(self.engine.actions[namespace][func].items())

        self.engine._script_engine(func, current_entity)

    def __staticAction(self, action):
        if action not in USER_STATIC_ACTION: return False

        match action:
            case "inventory": self.__staticaction_displayinventory()
            case "quit": exit()

        return True
    
    # --------------------------------------
    # STATIC ACTIONS
    # --------------------------------------
    def __staticaction_displayinventory(self):
        items = list(map(lambda x: x.name, self.inventory))
        items = ", ".join(items)
        self.engine.render(narration="You have: " + items, skip_next=True)

class PSEngine:
    def __init__(self, search_dir: str = "."):
        self.rooms = []
        self.world_flags = {}
        self.current_room = None
        self.player = Player()
        self.search_dir = search_dir
        self.world_dir = None
        self.engine_dir = os.path.split(__file__)[0]
        self.actions = {}
        self.render_skip_next = False
        
        self.player.engine = self

        with open(os.path.join(self.engine_dir, "builtin.json"), "r") as f:
            self.builtin = toDotdict(json.load(f))

    def loadWorld(self, world_name: str) -> None:
        """Loads a world folder

        Args:
            world_name (str): The world name. This should match a folder in the search directory

        Raises:
            WorldAlreadyLoadedException: A world is already loaded but is trying to load another.
            WorldNotFoundException: Cannot find the world folder in the search directory
        """

        self.world_dir = os.path.join(self.search_dir, world_name)

        if self.rooms != []: raise WorldAlreadyLoadedException("A world has already been loaded, unload it first and then load another.")
        if not os.path.exists(self.world_dir): raise WorldNotFoundException(f"The world folder '{world_name}' has not been found.")

        for file in os.listdir(self.world_dir):
            file = os.path.join(self.world_dir, file)

            if not os.path.isfile(file): continue
            if not file.endswith(".yaml"): continue

            with open(file, "r") as f:
                self.rooms.append(toDotdict(yaml.full_load(f)))

        if os.path.isfile(os.path.join(self.world_dir, "flags.json")):
            with open(os.path.join(self.world_dir, "flags.json"), "r") as f:
                self.world_flags = json.load(f)

        self.world_flags["_world_name"] = world_name

        self.__loadActionMap()
        self.__loadAddons()
        self.__loadActions()

    def unloadWorld(self) -> None:
        """Unload a world"""

        self.world_dir = None
        self.rooms = []
        self.world_flags = {}
        self.actions = {}

    def changeRoom(self, room: str | dict) -> None:
        """Change the current room

        Args:
            room (str | dict): The room to change to
        """

        if type(room) == str: self.current_room = self.findRoomByID(room)
        elif type(room) in [dict, dotdict]: self.current_room = room

    def findRoomByID(self, search_id: str) -> dict:
        """Find a room from a loaded world by the room id

        Args:
            search_id (str): The room ID

        Raises:
            RoomNotFoundException: A room with the provided room id doesn't exist in the loaded world

        Returns:
            dict: The room
        """

        for room in self.rooms:
            if room.id == search_id:
                return room
            
        raise RoomNotFoundException(f"Cannot find room with id: '{search_id}'")
            
    def findEntityByID(self, room: dict, search_id: str) -> dict:
        """Find an entity in a room

        Args:
            room (dict): The room to search
            search_id (str): The entity ID to search for

        Raises:
            EntityNotFoundException: The entity doesn't exist in the provided room

        Returns:
            dict: The entity
        """

        for entity in room.entities:
            if entity.id == search_id:
                return entity
            
        raise EntityNotFoundException(f"Cannot find entity with id '{search_id}' in room '{room.id}'")
    
    def findEntityByParameter(self, room: dict, param: str, target_value: str) -> dict:
        """Find an entity in a room

        Args:
            room (dict): The room to search
            param (str): The parameter to check the value of
            target_value (str): The expected value for the parameter

        Raises:
            EntityNotFoundException: The entity doesn't exist in the provided room

        Returns:
            dict: The entity
        """

        for entity in room.entities:
            try:
                if entity[param] == target_value:
                    return entity
            except KeyError:
                pass
            
        raise EntityNotFoundException(f"Cannot find entity which has parameter '{param}' set to '{target_value}'")
    
    def findEntityByCoords(self, room: dict, coords: list[int, int]) -> dict | None:
        """Find an entity in a room

        Args:
            room (dict): The room to search
            coords (list[int, int]): The coords to check

        Returns:
            dict | None: Returns the entity if found, otherwise None
        """
        
        for entity in room.entities:
            if entity.coords == coords:
                return entity
            
        return None
    
    def findItemInArrayByParameter(self, array: list, param: str, target_value: str) -> any:
        """Find an item in an array by its parameter

        Args:
            array (list): The array to search
            param (str): The parameter to check the value of
            target_value (str): The expected value for the parameter

        Raises:
            ItemNotFoundException: An item with that parameter set to the correct value doesn't exist in the array

        Returns:
            any: The item
        """

        for item in array:
            try:
                if item[param] == target_value:
                    return item
            except KeyError:
                pass
            
        raise ItemNotFoundException(f"Cannot find item in the array {array} which has parameter '{param}' set to '{target_value}'")
            
    def getRoomWH(self, room: dict) -> tuple[int, int]:
        """Get a rooms width and height

        Args:
            room (dict): The room

        Returns:
            tuple[int, int]: Width and height
        """
        
        return max(map(lambda x: len(x), room.layout.strip().split("\n"))), len(room.layout.strip().split("\n"))
        
    def render(self, room: dict = None, narration: str = None, skip_next: bool = False) -> None:
        """Renders a room

        Args:
            room (dict, optional): The room to render. Defaults to PSEngine.current_room
            narration (str, optional): Displays text instead of interactions. Defaults to None
            skip_next (bool, optional): Skips the next render call

        Raises:
            ValueError: Parameter missing
        """

        if self.render_skip_next:
            self.render_skip_next = False
            return

        if not room: room = self.current_room
        if not room: raise ValueError("'room' parameter is missing.")
        
        w, h = os.get_terminal_size()
        wr, hr = self.getRoomWH(room)
        buffer = io.StringIO()

        while not self.__canDraw(room):
            print(" Cannot fit map into the available terminal space. Please resize the terminal.", end="\r")
            time.sleep(0.25)

        w_half, h_half = w // 2, h // 2
        wr_half, hr_half = wr // 2, hr // 2
        TL = (w_half - wr_half - 2, h_half - hr_half - 2) # Top left, -2 to remove the borders
        with contextlib.redirect_stdout(buffer):
            # Draw to buffer
            print("+", end="")
            print("-" * (w - 2), end="")
            print("+", end="\r")
            print(f"+-- {AnsiColorCodes.Cyan}{room.name}{AnsiColorCodes.Reset}   {AnsiColorCodes.Red}{self.player.hp}{AnsiColorCodes.Reset}/{AnsiColorCodes.Red}{self.player.max_hp}{AnsiColorCodes.Reset} ")

            first_line = buffer.tell()
            chars_per_line = w + 1 # width + \n
            for line in range(1, h - 2):
                print("|", end="")
                print(" " * (w - 2), end="")
                print("|")

            print("+", end="")
            print("-" * (w - 2), end="")
            print("+", end="")

            # Draw map
            TL_Offset = first_line + (TL[1] * chars_per_line) + TL[0] # Go to first line, go to TL[1] (topleft.y) line, go to TL[0] (topleft.x) char
            buffer.seek(TL_Offset)
            for idx, line in enumerate(room.layout.strip().split("\n")):
                buffer.write(line)
                buffer.seek(TL_Offset + chars_per_line * (idx + 1))

            # Draw entities
            for entity in room.entities:
                if not entity.visible: continue

                try:
                    buffer.seek(TL_Offset + entity.coords[0] + entity.coords[1] * chars_per_line)
                    buffer.write(ETC_MAP[entity.type])
                except KeyError as e:
                    raise EntityNotFoundException(f"Entity {e} is not in the default set of entities, nor has it been loaded by a custom map.")

            # Draw player
            buffer.seek(TL_Offset + self.player.coords[0] + self.player.coords[1] * chars_per_line)
            buffer.write(ETC_MAP.player)

            if not narration:
                # Add interactions
                if (entity := self.findEntityByCoords(room, self.player.coords)):
                    if entity.visible:
                        buffer.seek(first_line + (h - 4) * chars_per_line + 2)
                        actions = entity.get("actions", {})
                        actions = list(filter(lambda x: x[1] != None, actions.items()))
                        actions = list(map(lambda x: x[0].title(), actions))
                        buffer.write(" | ".join(actions))
            else:
                # Add narration
                buffer.seek(first_line + (h - 4) * chars_per_line + 2)
                buffer.write("> " + narration)

        print(buffer.getvalue())

        if skip_next: self.render_skip_next = True

    def spawnPlayerAtRoot(self, room: dict) -> None:
        """Reset a player to the root spawn point. The root spawn point is identified by having no linked exit

        Args:
            room (dict): The room in which the player will spawn

        Raises:
            ValueError: A parameter is missing
            EntityNotFoundException: No unlinked spawn is present in the room
        """

        if not room: raise ValueError("'room' parameter is missing.")
        if not self.player: raise ValueError("'player' parameter is missing.")

        spawn = self.findEntityByParameter(room, "linked_exit", None)

        if not spawn: raise EntityNotFoundException(f"Cannot find an unlinked spawn in room '{room.name}'")

        self.player.coords = dc(spawn.coords)

    def inputLoop(self) -> str:
        """Pools the player for an input. W/A/S/D is returned for a simple command, and the full command name (ex. INSPECT/OPEN/CLOSE) is returned for the complex commands. Everything is sent in lowercase

        Returns:
            str: The key/action
        """

        while True:
            char = getch()
            
            if char.lower() in USER_BASIC_MOVEMENT:
                return char.lower()
                
            full = " "
            full += char.lower()
            while True:
                print(full, end="\r", flush=True)
                char = getch().lower()

                if char in ("\n", "\r"):
                    if full.strip() in USER_ADVANCED_MOVEMENT or full.strip() in USER_STATIC_ACTION:
                        return full.strip()

                    break

                full += char

            print(" " * MIN_TERM_WIDTH, end="\r", flush=True)

    def __canDraw(self, room):
        """Does the room fit into the terminal"""
        wr, hr = self.getRoomWH(room)
        w, h = os.get_terminal_size()

        if w < MIN_TERM_WIDTH: return False
        if w < wr + 4: return False
        if h < hr + 4: return False

        return True
    
    def __loadCustomActionMaps(self):
        maps = {"builtin": self.builtin.action_maps}

        if not os.path.exists(os.path.join(self.world_dir, "action_maps")): return maps

        for action_map in os.listdir(os.path.join(self.world_dir, "action_maps")):
            action_map = os.path.join(self.world_dir, "action_maps", action_map)

            if not os.path.isfile(action_map): continue

            with open(action_map, "r") as f:
                maps[os.path.splitext(action_map)[0]] = toDotdict(json.load(f))

        return maps

    def __loadActionMap(self):
        """Replaces action_map entries in entities with the correct actions from said mapping"""

        action_maps = self.__loadCustomActionMaps()

        for room in self.rooms:
            for entity in room.entities:
                if not entity.get("actions", {}).get("action_map", None): continue

                map_namespace, map_entity = entity.actions.action_map.split("/")
                replaced_map = dc(action_maps[map_namespace][map_entity])

                for action, func in entity.actions.items():
                    if action == "action_map": continue

                    replaced_map[action] = func

                entity.actions = replaced_map

    def __loadAddons(self):
        if not os.path.exists(os.path.join(self.world_dir, "addons")): return

        for addon in os.listdir(os.path.join(self.world_dir, "addons")):
            path = os.path.join(self.world_dir, "addons", addon)

            if not os.path.isfile(path): continue

            with open(path, "r") as f:
                loaded = json.load(f)

                for entity, char in loaded.get("etc_map", {}).items():
                    ETC_MAP[entity] = char

                for item in loaded.get("uam", []): # User Advanced Movement
                    USER_ADVANCED_MOVEMENT.append(item)

    def __loadBaseActions(self):
        self.actions["builtin"] = {}

        for name, func in self.builtin.actions.items():
            parsed = yaml.full_load(func)
            self.actions["builtin"][name] = parsed

        self.actions = toDotdict(self.actions)

    def __loadActions(self):
        self.__loadBaseActions()
        
        if not os.path.exists(os.path.join(self.world_dir, "actions")): return
        
        for action in os.listdir(os.path.join(self.world_dir, "actions")):
            path = os.path.join(self.world_dir, "actions", action)
            namespace = os.path.splitext(action)[0]

            if not os.path.isfile(path): continue

            with open(path, "r") as f:
                loaded = yaml.full_load(f)

                for name, func in loaded.items():
                    self.actions[namespace] = {}
                    self.actions[namespace][name] = func

        self.actions = toDotdict(self.actions)

    def __buildStateMap(self, current_entity, current_item):
        player_map = {"inventory": self.player.inventory, "coords": {"x": self.player.coords[0], "y": self.player.coords[1]}, "hp": self.player.hp, "max_hp": self.player.max_hp, "level": self.player.level}
        state_map = {"rooms": self.rooms, "current_room": self.current_room, "flags": self.world_flags, "current_entity": current_entity, "current_item": current_item, "player": player_map}
        return state_map
    
    def __renderTemplate(self, template, state_map, skip_last=0):
        # Renders the template only, does not assing. Returns the sub-indexed whatnot state_map
        #cur_state_map = dc(state_map)
        items = template.split(".")
        end = len(items) if skip_last == 0 else -skip_last

        for item in items[:end]:
            if "[" in item:
                start = item.index("[")
                extracted = item[start + 1:-1]

                if extracted.isnumeric():
                    # Get item at index
                    state_map = state_map[item[:start]]
                    state_map = state_map[int(extracted)]
                else:
                    # Get item with parameter
                    param, value = extracted.split(":")
                    state_map = state_map[item[:start]]
                    state_map = self.findItemInArrayByParameter(state_map, param, value)
            else:
                state_map = state_map[item]

        return state_map, items[-1]
    
    def __isTemplate(self, template):
        if template == True or template == False: return False # Bool
        if template.isnumeric(): return False # Number
        if template.startswith("STR:"): return False # String

        return True # Might leave some edge cases

    def __parseImmediate(self, text):
        if type(text) == bool: return text
        if text.isnumeric(): return int(text)
        return text.replace("STR:", "")
    
    def _handlerExists(self, handler, action):
        namespace, func = handler.split("/")

        if namespace not in self.actions: raise HandlerNotFoundException(f"Handler for '{action}' is not in the default set of handlers, nor has it been loaded by a custom addon.")
        if func not in self.actions[namespace]: raise HandlerNotFoundException(f"Handler for '{action}' is not in the default set of handlers, nor has it been loaded by a custom addon.")

        return namespace, func

    def _script_engine(self, script, current_entity):
        queue = []
        current_item = None
        item_array = None
        flag_manual_break = False
        while script:
            entry, data = script.pop(0) # Entry is what to do, data is data passed to the entry.
            entry = entry.split("#")[0]

            match entry:
                case "display_text": self.__action_displaytext(data, current_entity, current_item)
                case "show_content": self.__action_showcontent(data, current_entity, current_item)
                case "set": self.__action_set(data, current_entity, current_item)
                case "add": self.__action_add(data, current_entity, current_item)
                case "remove": self.__action_remove(data, current_entity, current_item)
                case "break": flag_manual_break = True
                case "raise":
                    handler = self.__action_raise(data, current_entity, current_item)
                    namespace, new_func = self._handlerExists(handler, data)
                    #new_func = list(self.engine.actions[namespace][new_func].items())
                    #for call, call_data in new_func[::-1]:
                    #    script.insert(0, (call, call_data))
                case "if":
                    status = self.__action_if(data, current_entity, current_item)

                    if status:
                        for call, call_data in list(data.exec.items())[::-1]:
                            script.insert(0, (call, call_data))
                case "else":
                    if not status:
                        status = True
                        for call, call_data in list(data.items())[::-1]:
                            script.insert(0, (call, call_data))
                case "for":
                    flag_break = False
                    if data.iter == "CONT":
                        index = item_array.index(current_item)
                        index += 1

                        if index == len(item_array):
                            flag_break = True
                        else:
                            current_item = item_array[index]
                    else:
                        item_array = dc(self.__action_for(data, current_entity)) # Unlink to allow for modification while running
                        if len(item_array) > 0: current_item = item_array[0]
                        else: flag_break = True

                    if flag_manual_break:
                        flag_break = True
                        flag_manual_break = False

                    if not flag_break:
                        for call, call_data in list(data.exec.items())[::-1]:
                            script.insert(0, (call, call_data))

                        script.insert(0, ("for", toDotdict({"iter": "CONT", "exec": data.exec})))

        for item, entity in queue:
            self._script_engine(item, entity)

    # --------------------------------------
    # ACTIONS
    # --------------------------------------
    def __action_displaytext(self, params, current_entity, current_item):
        state_map = self.__buildStateMap(current_entity, current_item)
        
        if params.get("text", None):
            self.render(narration=params.text, skip_next=True)
        elif params.get("text_template", None):
            try:
                cur_state_map = self.__renderTemplate(params.text_template, state_map)[0]
            except KeyError as e:
                raise InvalidTemplateException(f"Action: display_text\nTemplate: {params.text_template}\nInvalid field: {e}\n\nValues:\nstate_map: {state_map}")
                
            if type(cur_state_map) == str or type(cur_state_map) == int:
                self.render(narration=cur_state_map, skip_next=True)
            else:
                raise InvalidTemplateException(f"Action: display_text\nTemplate: {params.text_template}\nFinal value: {cur_state_map}\nFinal value is not an acceptable type\nType is: {type(cur_state_map)}, accetable is str or int\n\nValues:\nstate_map: {state_map}")

    def __action_showcontent(self, template, current_entity, current_item):
        state_map = self.__buildStateMap(current_entity, current_item)
        content = self.__renderTemplate(template, state_map)[0]
        content_names = list(map(lambda x: x.name, content))
        content_str = ", ".join(content_names)
        content_str = "Contents: " + content_str

        self.render(narration=content_str, skip_next=True)

    def __action_set(self, params, current_entity, current_item):
        state_map = self.__buildStateMap(current_entity, current_item)
        fields, last = self.__renderTemplate(params.field, state_map, 1)
        fields[last] = params.value

    def __action_add(self, params, current_entity, current_item):
        state_map = self.__buildStateMap(current_entity, current_item)
        field = self.__renderTemplate(params.field, state_map)[0]

        if type(field) != list:
            raise InvalidTemplateException(f"Action: for\nTemplate: {params.field}\nFinal value: {field}\nFinal value is not an acceptable type\nType is: {type(field)}, accetable is list\n\nValues:\nstate_map: {state_map}")

        if params.get("value", None):
            field.append(params.value)
        elif params.get("value_template", None):
            field.append(self.__renderTemplate(params.value_template, state_map)[0])

    def __action_remove(self, params, current_entity, current_item):
        state_map = self.__buildStateMap(current_entity, current_item)
        field = self.__renderTemplate(params.field, state_map)[0]

        if type(field) != list:
            raise InvalidTemplateException(f"Action: for\nTemplate: {params.field}\nFinal value: {field}\nFinal value is not an acceptable type\nType is: {type(field)}, accetable is list\n\nValues:\nstate_map: {state_map}")

        if params.get("idx", None):
            del field[params.idx]
        elif params.get("param", None):
            param, value = params.param.split(":")
            item = self.findItemInArrayByParameter(field, param, self.__parseImmediate(value))
            field.remove(item)

    def __action_raise(self, template, current_entity, current_item):
        state_map = self.__buildStateMap(current_entity, current_item)
        handler = self.__renderTemplate(template, state_map)[0]
        return handler

    def __action_if(self, params, current_entity, current_item):
        state_map = self.__buildStateMap(current_entity, current_item)
        a_status = self.__isTemplate(params.a)
        b_status = self.__isTemplate(params.b)

        if a_status: a = self.__renderTemplate(params.a, state_map)[0]
        else: a = self.__parseImmediate(params.a)

        if b_status: b = self.__renderTemplate(params.b, state_map)[0]
        else: b = self.__parseImmediate(params.b)

        match params.op:
            case "==":
                if a == b: return True
            case "!=":
                if a != b: return True
            case "<":
                if a < b: return True
            case ">":
                if a > b: return True
            case "<=":
                if a <= b: return True
            case ">=":
                if a >= b: return True

        return False
    
    def __action_for(self, params, current_entity):
        state_map = self.__buildStateMap(current_entity, None)
        array = self.__renderTemplate(params.iter, state_map)[0]

        if type(array) != list:
            raise InvalidTemplateException(f"Action: for\nTemplate: {params.iter}\nFinal value: {array}\nFinal value is not an acceptable type\nType is: {type(array)}, accetable is list\n\nValues:\nstate_map: {state_map}")

        return array
