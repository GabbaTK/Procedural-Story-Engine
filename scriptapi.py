class API():
    def __init__(self, engine):
        self.engine = engine

    def getPlayerHP(self) -> int:
        return self.engine.player.hp
    def getPlayerMaxHP(self) -> int:
        return self.engine.player.max_hp
    def getPlayerLevel(self) -> int:
        return self.engine.player.level
    def getPlayerInventory(self) -> list[dict]:
        return self.engine.player.inventory
    def changePlayerHP(self, value):
        self.engine.player.hp += value
        return self.engine.player.hp
    def changePlayerMaxHP(self, value):
        self.engine.player.max_hp += value
        return self.engine.player.max_hp
    def changePlayerLevel(self, value):
        self.engine.player.level += value
        return self.engine.player.level
    def setPlayerHP(self, value):
        self.engine.player.hp = value
    def setPlayerMaxHP(self, value):
        self.engine.player.max_hp = value
    def setPlayerLevel(self, value):
        self.engine.player.level = value
