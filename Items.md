# PSE Items

This file describes the schema for some items. For each item there is a JSON that describes its parameters.
ID is always the item, UID is a configurable UserID that can be used to discern a specific item from the others, name is a player friendly name.

## Key
`lock_id` is used to differentiate keys, ie. which key can lock/unlock what entity.
```json
{
    "id": "key",
    "name": "Key",
    "uid": null,
    "lock_id": null
}
```
