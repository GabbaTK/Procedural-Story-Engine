# Entry Program — main.py

A minimal entry program for the Procedural Story Engine (PSEngine). This demo shows the smallest runnable setup to load a world, place the player, and run a simple input loop. Developers/players can replace or extend this file with more complex startup logic.

## Purpose
 - Demonstrate how to initialize the engine and load a world.
 - Provide a tiny example game loop with basic movement and action dispatch.

## Behavior (summary)
1. Create the engine instance:
    ```python
    Engine = engine.PSEngine()
    ```
2. Load a world:
    ```python
    Engine.loadWorld("Demo World")
    ```
3. Find and enter the starter room:
    ```python
    starter_room = Engine.findRoomByID("starter_room")
    Engine.changeRoom(starter_room)
    ```
4. Spawn the player at the room root:
    ```python
    Engine.spawnPlayerAtRoot()
    ```
5. Main loop:
    ```python
    Engine.render()
    act = Engine.inputLoop()
    match act:
        case "w": Engine.player.moveUp()
        case "a": Engine.player.moveLeft()
        case "s": Engine.player.moveDown()
        case "d": Engine.player.moveRight()
        case _: Engine.player.doAction(act)
        ```

## Controls
 - Movement: w (up), a (left), s (down), d (right)
 - Other inputs are passed to player.doAction for custom behavior.

## Extending this entry program
 - Load a different world or accept a world name from CLI args.
 - Add startup scripts, global state, or debugging output.
 - Customize player spawn location (use other room IDs or coordinates).
 - Replace the simple match with a richer input parser or command system.
 - Integrate UI elements or multiplayer hooks.

This file is intentionally minimal. Copy it as a starting template and expand as needed.