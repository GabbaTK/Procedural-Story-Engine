# PSE Schema

This file describes the schema for the world file

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
 - blocking_tiles: Tiles which block the players movements

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
A detailed guide on how to create functions is described [here](YamlFunctions.md)

## Scripts
Scripts are python files that run when called from a yaml function. Scripts may be referenced in the schema by other names, such as `modules` or `plugins`
A detailed guide on how to create scripts is described [here](CustomScripts.md)

---

## Room

```yaml
Room:
  id: string # Unique room identifier
  name: string # Player-friendly display name
  layout: string # 2D text layout without entities
  entities: Entity[] # Entities present in room
  generators: RoomGeneratorConfig[] # One config per exit
```

## Entity
`action_map` is the default map of actions for the entities, actions can then be overwritten, added or removed.
To add or change an action, the parameter is the `namespace/handler` function which will run when that action happens.
To remove an action, set the parameter to `null`.
Events are defined with `event_name: namespace/handler`. Events happen when code raises an event. When an event is raised, the associated handler function is ran.
Coords start at 0 in the top left corner.

### Dummy
The dummy does not do anything. You can add any properties, actions, events, parameters you want. The dummy will never render on the map, thus, the visible property must always be set to false.
```yaml
Dummy:
  type: "dummy"
  visible: false
```

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
    action_name: namespace/function, optional
  events: # optional
    event_name: event_handler
```

### Item
The `data` property describes the item. `id` is always required and is the item identifier, and `name` is the player friendly name. `other_item_data` depends on the chosen item.
If the item is from the default set of items described [here](Items.md), then you can use the described properties.
If the item is not in the default set of items, then you must define the properties yourself.
```yaml
Item:
  type: "item"
  coords: int[2]
  visible: bool
  properties:
    inspect_text: string
    data:
      id: string
      name: string
      other_item_data: other_item_data
  actions:
    action_map: "builtin/item", optional
    action_name: namespace/function, optional
```

### Exit
```yaml
Exit:
  type: "exit"
  id: string # To differentiate between exits
  coords: int[2]
  visible: bool
  actions:
    action_map: "builtin/exit", optional
    action_name: namespace/handler, optional
```

### Spawn Point
```yaml
SpawnPoint:
  type: "spawn_point"
  linked_exit: string # ID of the exit that leads to this spawn point. null if ths is the default spawn point
  coords: int[2]
  visible: bool
```

## Generators
Generators describe what room will be generated when a player leaves through an exit.
Each generator can have an associated exit id, meaning, that generator will only run if the player exited through that exit. If this is not used, set the `exit` paramter to `null`
`exit: null` is a match all case, so if you want to match specific exits first, put those generators above the match all generator to ensure that those generators run instead of the match all.

### Forced
```yaml
RoomGeneratorConfig:
  exit: string # Exit identifier
  type: "forced"
  room: string # Target room ID
```

### Conditional
```yaml
RoomGeneratorConfig:
  exit: string # Exit identifier
  type: "conditional"
  conditions:
    - type: if
      a: something
      op: something
      b: something
      room: string # If evaluates to true, change to this room
    - type: if # Multiple if statements can be added
    - type: room
      room: string # Default if no condition matches
```

### Random
If you want to dynamically change the weight, you can either set it to a value by using the [`set`](YamlFunctions.md#calls) call, or increment/decrement it by changing the weight directly in the loaded room via a [plugin](CustomScripts.md)
```yaml
RoomGeneratorConfig:
  exit: string # Exit identifier
  type: "random"
  pool:
    - room: string # Room ID
      weight: number
```

### Plugin
```yaml
RoomGeneratorConfig:
  exit: string # Exit identifier
  type: "plugin"
  handler: string # Module function reference
```
