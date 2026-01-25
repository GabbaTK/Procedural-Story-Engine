# PSE Schema

## World
A world consists of a folder containing all of the rooms and data.
An example of a world is:
```
MyWorld
 |- RoomA.yaml
 |- RoomB.yaml
 |- flags.json
 |- addons
 |   |- myaddon.json
 |   |- anotheraddon.json
 |- action_maps
 |   |- mymap.json
 |   |- anothermap.json
 |- actions
 |   |- myaction.yaml
 |   |- anotheraction.yaml
 |- scripts
 |   |- myscript.py
 |   |- anotherscript.py

```
## Flags
World flags can be set to a default value in the `flags.json` file

## Addons
Addons can change some functionality of the engine, like adding more entities, or more commands.
To define an addon, create a json in the `addons` folder. The following keys can be used to change the functionality:
 - etc_map: Contains a dict where the key is the entity type, and the value is the character to render for that entity.
 - uam: Adds more commands that the player can type.
 - entities: Custom entities

## Actions Maps
Action maps allow developers to quickly define actions for entities from pre-defined maps.
To create an action map, create a json in the `action_maps` folder. The file name is the namespace for the mapping.
The key is the mapping, and the value is another dictionary where the key is the action, and the value is the `namespace/handler` function for that action.

## Actions
To create a custom action or replace the built-in handler, create a yaml file inside the `actions` folder. The file name is the namespace for the action.
Syntax for a function is as follows:
```yaml
MyFunction:
  callA:
    paramA: something
    paramB: something
  callB:
    param: something-else
```

### Calls
If you have multiple same calls on the same level you can suffix them with `#something-unique`.
`If Else` statements are not context aware, meaning, if you have a nested if statement, the inner one will overwrite if the `else` will happen. So even though the first `if` happend, so naturally the else should run, if the second if doesn't run, the `else` will still run.

```yaml
display_text:
  text: Text to display (provide either text or text_template, not both)
  text_template: Template to render out
```
```yaml
show_content: Template of a container
```
```yaml
set:
  field: Field to change (Last entry in the template cannot be an index or paramter search)
  value: Value to set to
```
```yaml
if:
  a: First parameter (To check against a string, prefix it with 'STR:')
  op: Operation (==, !=, >, <, >=, <=)
  b: Second parameter (To check against a string, prefix it with 'STR:')
  exec:
    Calls (Same syntax as functions)
```
```yaml
else:
  Calls (Same syntax as functions)
```
```yaml
for:
  iter: Template to render out. Must render out to a list
  exec:
    Calls (Same syntax as function)
```
```yaml
add:
  field: Field to append to
  value: Value to add
  value_template: Value to add from the state_map
```
```yaml
remove:
  field: Field to remove an element
  idx: Index of the element to remove
  param: param:value
```
```yaml
raise: template_to_event
```
```yaml
py: name_of_script_without_extension:name_of_function
```

### Templates
Templates look like this:
 - a.b.c.d          -> Indexes normally
 - a.b[0]           -> Gets the first element of `b`
 - a.b[id:someid]   -> Gets the first element of `b` which has a parameter `id` set to `someid`

Templates index the state_map, which is generated per action call. The state map contains these items:
 - rooms            -> All loaded rooms in this world
 - current_room     -> The current room
 - flags            -> World flags
 - current_entity   -> The entity that the player is standing on
 - current_item     -> If in a for loop, this is the current element being iterated. Changes to this item do not save in the main state_map
 - player
    - inventory
    - coords
       - x
       - y
    - hp
    - max_hp
    - level

### World Flags
World flags contain data shared across all rooms. The flags are mainly changed via functions, but there are some flags provideded by PSE:
 - _world_name -> The name of the world

---

## Room

```yaml
Room:
  id: string (Unique room identifier)
  name: string (Player-friendly display name)
  layout: string (2D text layout without entities)
  entities: Entity[] (Entities present in room)
  events: Event[] (Events that can trigger)
  generator: RoomGeneratorConfig[] (One config per exit)
```


## Entity
`action_map` is the default map of actions for the entities, actions can then be overwritten, added or removed.
To add or change an action, the parameter is the `namespace/handler` function which will run when that action happens.
To remove an action, set the parameter to `null`.
Events are defined with `event_name: namespace/handler`. Events happen when code raises an event. When an event is raised, the associated handler function is ran.

### Chest
```yaml
Chest:
  type: "chest"
  coords: int[2]
  visible: bool
  properties:
    inspect_text: string
    open: bool
    locked: bool
    can_lock: bool, optional
    key_id: string, optional
    contents: Item[]
  actions:
    action_map: "builtin/chest", optional
    inspect: string, optional
    open: string, optional
    close: string, optional
    lock: string, optional
    unlock: string, optional
    gather: string, optional
  events: (optional)
    event_name: event_handler
```

### Spawn Point
```yaml
SpawnPoint:
  type: "spawn_point"
  linked_exit: string (ID of the exit that leads to this spawn point)
  coords: int[2]
  visible: bool
```
