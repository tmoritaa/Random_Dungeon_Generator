import json
from randDungGen import Dungeon, GridEnum

class RandDungJsonParser(object):
    def __init__(self, fileName):
        f = open(fileName)
        self.readObj = json.load(f)
        
    def retrieveDungeon(self):
        width = self.readObj["width"]
        height = self.readObj["height"]
        dungeon = Dungeon(width, height)

        rooms = self.readObj["rooms"]
        doors = self.readObj["doors"]

        for room in rooms:
            for y in xrange(room["y1"], room["y2"]):
                for x in xrange(room["x1"], room["x2"]):
                    dungeon.grid[y][x] = GridEnum.FLOOR
            
        for door in doors:
            doorWidth = door['w']
            xPos = door['x']
            yPos = door['y']
            if door['dir'] == 'v':
                for y in xrange(yPos, yPos + doorWidth):
                    dungeon.grid[y][xPos] = GridEnum.DOOR
            if door['dir'] == 'h':
                for x in xrange(xPos, xPos + doorWidth):
                    dungeon.grid[yPos][x] = GridEnum.DOOR

        return dungeon

if __name__ == "__main__":
    randDungJsonParser = RandDungJsonParser('dungeonInfo.json')
    dungeon = randDungJsonParser.retrieveDungeon()
    for y in xrange(0, dungeon.height):
        s = ""
        for x in xrange(0, dungeon.width):
            s += str(dungeon.grid[y][x]) + " "
        print s.strip()
