# Custom Scripts

This file documents the framework for adding custom python scripts to the world.

## API
You can import the scripting api by running:
```python
def init(engine):
    global api
    api = engine.script_api
```
The full engine is provided so you _can_ call non api functions, but that **is not** recommended.

### API Endpoints
| Function | Input | Output | Description |
| -------- | ----- | ------ | ----------- |
| getPlayerHP | | int | Players HP |
| getPlayerMaxHP | | int | Players maximum HP |
| getPlayerLevel | | int | Players level |
| getPlayerInventory | | list[dict] | Get the players inventory. Each element is a dict with contentes described in [Items.md](Items.md) |
| changePlayerHP | int | int | Inputs the amount to change, can be positive or negative. Outputs the new value |
| changePlayerMaxHP | int | int | Inputs the amount to change, can be positive or negative. Outputs the new value |
| changePlayerLevel | int | int | Inputs the amount to change, cna be positive or negative. Outputs the new value |
| setPlayerHP | int | | Set the players HP to a new value |
| setPlayerMaxHP | int | | Set the players maximum HP to a new value |
| setPlayerLevel | int | | Set the players level to a new value |