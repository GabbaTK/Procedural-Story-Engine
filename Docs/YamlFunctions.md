# Yaml Functions

This file documents on how to create custom yaml functions

## Creating
To create a function, follow [this schema](Schema.md#actions)

## Calls
If you have multiple same calls on the same level you can suffix them with `#something-unique`.
`If Else` statements are not context aware, meaning, if you have a nested if statement, the inner one will overwrite if the `else` will happen. So even though the first `if` happend, so naturally the else should run, if the second if doesn't run, the `else` will still run.

```yaml
display_text:
  text: Text to display # provide either text or text_template, not both
  text_template: Template to render out
```
```yaml
show_content: Template of a container
```
```yaml
set:
  field: Field to change # Last entry in the template cannot be an index or paramter search
  value: Value to set to
  value_template: Template to render out
```
```yaml
if:
  a: First parameter # To check against a string, prefix it with 'STR:'
  op: Operation # ==, =!, >, <, >=, <=, can be a template
  b: Second parameter # To check against a string, prefix it with 'STR:'
  exec:
    Calls # Same syntax as functions
```
```yaml
else:
  Calls # Same syntax as functions
```
```yaml
for:
  iter: Template to render out. Must render out to a list
  exec:
    Calls # Same syntax as function
```
```yaml
break: null # Breaks from the current for loop, will still finish all the functions in exec:
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

py: TEMP:template
```
```yaml
change_room: room_id # Supports templates, if its not a template, prefix it with 'STR:'
```
```yaml
# This automatically adds all the options present and returns a random choice
random:
  option_a: weight # Key can be a template, if its a string, prefix it with 'STR:'. Key will be returned in flags._random if its picked
  option_b: weight # Key can be a template, if its a string, prefix it with 'STR:'. Key will be returned in flags._random if its picked

# This is only required for dynamic adding/with a queue
random:
  action: reset (Resets the choices)

random:
  action: add (Add a single option to the list of choices)
  data:
    option_a: weight
    option_b: weight

random:
  action: start (Picks a choice at random)
```
```yaml
spawn_player: exit_id # Spawns the player at the associated spawn with the provided exit id. If no spawn exists, spawns them at the default spawn. Can be a template, if not, prefix with 'STR:'
```
```yaml
damage_player: amount # To do dynamic damage, put a template
```
```yaml
heal_player: amount # To do dynamic healing, put a template
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
 - _random -> Returns the randomly picked entry

### Builtin Function World Flags
These flags are changed by the built in functions, it is not recommended to use them for your own purposes.
If you are using your own functions instead of the built in ones, you are free to then use these flags. Just make sure that no other function uses them
 - loop_found_val
