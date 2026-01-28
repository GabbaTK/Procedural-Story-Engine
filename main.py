import updater
import engine

Engine = engine.PSEngine()

print("This is a minimal program to demonstarate the engines capabilities.")
Engine.loadWorld("Demo World")

starter_room = Engine.findRoomByID("starter_room")
Engine.changeRoom(starter_room)
Engine.spawnPlayerAtRoot()

while True:
    Engine.render()
    act = Engine.inputLoop()
    
    match act:
        case "w": Engine.player.moveUp()
        case "a": Engine.player.moveLeft()
        case "s": Engine.player.moveDown()
        case "d": Engine.player.moveRight()
        case _: Engine.player.doAction(act)
