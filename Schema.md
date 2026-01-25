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
Scripts are python files that run when called from a yaml function.
A detailed guide on how to create scripts is described [here](CustomScripts.md)

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
