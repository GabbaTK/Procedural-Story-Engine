# Yaml Functions

This file documents on how to create custom yaml functions

## Creating
To create a function, follow [this schema](Schema.md#actions)

## Calls
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

## Templates
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

## World Flags
World flags contain data shared across all rooms. The flags are mainly changed via functions, but there are some flags provideded by PSE:
 - _world_name -> The name of the world