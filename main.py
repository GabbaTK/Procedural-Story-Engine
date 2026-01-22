import engine

Engine = engine.PSEngine()

Engine.loadWorld("TestWorld")

starter_room = Engine.findRoomByID("starter_room")
Engine.spawnPlayerAtRoot(starter_room)
Engine.changeRoom(starter_room)

while True:
    Engine.render()
    act = Engine.inputLoop()

    match act:
        case "w": Engine.player.moveUp()
        case "a": Engine.player.moveLeft()
        case "s": Engine.player.moveDown()
        case "d": Engine.player.moveRight()
        case _: Engine.player.doAction(act)
