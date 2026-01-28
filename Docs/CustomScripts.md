# Custom Scripts

This file documents the framework for adding custom python scripts to the world.

## Coding
Minimal script:

`MyScript.py`
```python
def init(engine):
    global eng
    eng = engine

def onLoad(): ...
def onRender(): ...
```

In this example, to call `myFunction`, you would do:
```yaml
py: MyScript:myFunction
```

You have access to the full engine. To create scripts you manipulate the engine directly. Make sure you have a good understanding of the engine so you do not accidentally break something.

## Other Functions
 - onLoad -> Runs when a room change occurs
 - onRender -> Runs when `engine.render()` is called. Runs before the actual render loop
These functions are required. If they are not used, put empty functions
