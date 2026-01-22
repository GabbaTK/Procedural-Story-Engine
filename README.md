# PSE - Procedural Story Engine

PSE is a **modular, console-based narrative engine** built around handcrafted rooms, dynamic generation, and emergent gameplay. It’s designed to feel like a world you _explore_, not a script you follow.

The engine prioritizes **replayability** and **modularity** over realism or production-scale complexity. Rooms are mostly hand-crafted, but how they connect, what appears inside them, and how they react to player history is driven by configuration and states, not hardcoded logic.

## What PSE Is

- A **visual console engine** where rooms are rendered as text grids
- A **story/world engine**, not a one-off game
- A system where **the same room can behave differently** depending on how the player got there
- A foundation that supports **plugins, extensions, and experimentation**

PSE is meant to be fun to build *and* fun to revisit months or years later.

## Core Ideas

### Handcrafted Rooms, Dynamic Worlds
Rooms are created manually, but:
- Entities can appear, disappear, or change
- Exits can lead to different places based on history or states

### Exit-Based World Generation
When a player leaves a room into the unknown, PSE doesn’t just _pick a random room_.

Instead, exits are resolved through:
- Forced transitions  
- Conditional logic (based on flags, items, past actions)  
- Weighted random pools  
- Plugin-defined resolvers  

This allows the world to react to what the player has already done.

### Entity-Driven Interaction
Everything interactive is an **entity**:
- Chests
- NPCs
- Doors
- Mechanisms
- Items
- Plugin-defined objects

Entities expose:
- **Properties**  (state)
- **Actions**     (what the player can do)

Rooms don’t contain logic. They describe _what exists_. Behavior emerges from entity rules and world state.

### Modular by Design
PSE is built so that:
- New rooms can be added without touching the engine
- New entities can be introduced via plugins
- Generation rules can evolve independently of room content

The engine exposes state and rendering hooks, but doesn’t assume what you’ll build with them.

## What PSE Is _Not_

- Not a graphical game engine  
- Not a full roguelike framework  
- Not a pre-crafted story with fixed outcomes  
- Not a single _finished_ game  

PSE is a **toolbox for building reactive, text-based worlds**.

---

> **Note**  
> Instructions for creating rooms, entities, generators, and plugins live in separate documentation files.  
> This README is intentionally conceptual.
