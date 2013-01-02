import random
import json

class GridEnum(object):
    WALL = 0
    FLOOR = 1
    DOOR = 2

class Dungeon(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[GridEnum.WALL]*height for x in xrange(width)]

class RandDungGen(object):
    def __init__(self, inpFileName):
        self.dungWidth = 0
        self.dungHeight = 0
        self.minRoomNum = 0
        self.maxRoomNum = 0
        self.minRoomWidth = 0
        self.maxRoomWidth = 0
        self.minRoomHeight = 0
        self.maxRoomHeight = 0
        self.minDoorWidth = 0
        self.maxDoorWidth = 0
        self.retryCount = 0

        self._readInputFile(inpFileName)

        self.dungeonInfo = {}
        self.dungeonInfo["rooms"] = {}
        self.dungeonInfo["doors"] = {}
        self.dungeonInfo["width"] = self.dungWidth
        self.dungeonInfo["height"] = self.dungHeight

        self.dungeon = Dungeon(self.dungWidth, self.dungHeight)

        self.genNewDungeon()

    def _readInputFile(self, inpFileName):
        inpFile = open(inpFileName, 'r') 

        for line in inpFile:
            tokens = line.strip().split(' ')
            if tokens[0] == "dungWidth":
                self.dungWidth = int(tokens[1])
            elif tokens[0] == "dungHeight":
                self.dungHeight = int(tokens[1])
            elif tokens[0] == "minRoomNum":
                self.minRoomNum = int(tokens[1])
            elif tokens[0] == "maxRoomNum":
                self.maxRoomNum = int(tokens[1])
            elif tokens[0] == "minRoomWidth":
                self.minRoomWidth = int(tokens[1])
            elif tokens[0] == "maxRoomWidth":
                self.maxRoomWidth = int(tokens[1])
            elif tokens[0] == "minRoomHeight":
                self.minRoomHeight = int(tokens[1])
            elif tokens[0] == "maxRoomHeight":
                self.maxRoomHeight = int(tokens[1])
            elif tokens[0] == "minDoorWidth":
                self.minDoorWidth = int(tokens[1])
            elif tokens[0] == "maxDoorWidth":
                self.maxDoorWidth = int(tokens[1])
            elif tokens[0] == "retryCount":
                self.retryCount = int(tokens[1])

    def genNewDungeon(self):
        # plop one room
        roomNum = 1
        roomW = random.randint(self.minRoomWidth, self.maxRoomWidth)
        roomH = random.randint(self.minRoomHeight, self.maxRoomHeight)

        anchorX = random.randint(0, self.dungeon.width - roomW)
        anchorY = random.randint(0, self.dungeon.height - roomH)

        for x in xrange(anchorX, roomW + anchorX):
            for y in xrange(anchorY, roomH + anchorY):
                self.dungeon.grid[y][x] = GridEnum.FLOOR

        self.dungeonInfo["rooms"][roomNum] = {"x1":anchorX, "y1":anchorY, 
                                "x2":roomW + anchorX, "y2":roomH + anchorY}

        # wall info format (loc. in room, unchanging x/y coor, 
        #               changing x/y coor, width/height)
        wallList = []
        allWallList = []
        
        wallList.append(('l', anchorX - 1, anchorY, roomH))
        wallList.append(('r', anchorX + roomW, anchorY, roomH))
        wallList.append(('u', anchorY - 1, anchorX, roomW))
        wallList.append(('d', anchorY + roomH, anchorX, roomW))

        allWallList.extend(wallList)
        # for each (wall of room, decide whether to gen new room)
        retryCount = 0
        while len(wallList) and roomNum < self.maxRoomNum \
                or roomNum < self.minRoomNum:
            if len(wallList) == 0:
                retryCount += 1
                wallList.extend(allWallList)

            if retryCount >= self.retryCount:
                break
            
            wall = wallList.pop(0)

            # randomly determine whether to gen room on this wall
            if random.randint(0, 1):
                continue

            # randomly determine dimension of room
            roomW = random.randint(self.minRoomWidth, self.maxRoomWidth)
            roomH = random.randint(self.minRoomHeight, self.maxRoomHeight)

            direction = wall[0]
            uncCor = wall[1]
            cCor = wall[2]
            dim = wall[3]

            wallAnchor = random.randint(cCor + 1, cCor + dim - 1)
            x1 = 0
            x2 = 0
            y1 = 0
            y2 = 0
            # randomly determine anchor point on wall
            if direction == 'l' or direction == 'r':
                y1 = wallAnchor - roomH/ 2 
                y2 = wallAnchor + roomH / 2
                y2 += 1 if roomH % 2 != 0 else 0
                if direction == 'l':
                    x1 = uncCor - roomW
                    x2 = uncCor
                elif direction == 'r':
                    x1 = uncCor + 1
                    x2 = uncCor + roomW + 1
            elif direction == 'u' or direction == 'd':
                x1 = wallAnchor - roomW / 2
                x2 = wallAnchor + roomW / 2
                x2 += 1 if roomW % 2 != 0 else 0
                if direction == 'u':
                    y1 = uncCor - roomH
                    y2 = uncCor
                elif direction == 'd':
                    y1 = uncCor + 1
                    y2 = uncCor + roomH + 1
               
            # check if out of bounds
            if x1 < 0 or x2 >= self.dungeon.width or \
                y1 < 0 or y2 >= self.dungeon.height:
                continue

            # check if overlapping
            placeable = True
            for x in xrange(x1, x2):
                for y in xrange(y1, y2):
                    if self.dungeon.grid[y][x] != GridEnum.WALL:
                        placeable = False
                        break
            
            # if not placeable, go to next wall
            if not placeable:
                continue

            # create room
            roomNum += 1
            for x in xrange(x1, x2):
                for y in xrange(y1, y2):
                    self.dungeon.grid[y][x] = GridEnum.FLOOR

            self.dungeonInfo["rooms"][roomNum] = {"x1":x1, "y1":y1, 
                                            "x2":x2, "y2":y2}

            # if successful, push room onto next gen root queue
            wallList.append(('l', x1 - 1, y1, roomH))
            wallList.append(('r', x2, y1, roomH))
            wallList.append(('u', y1 - 1, x1, roomW))
            wallList.append(('d', y2, x1, roomW))
            allWallList.extend(wallList)

            # generate door
            # randomly set door and walls based on anchor point
            doorWidth = random.randint(self.minDoorWidth, 
                self.maxDoorWidth)

            # get x and y for passageway
            passX1 = 0
            passX2 = 0
            passY1 = 0
            passY2 = 0
            if direction == 'l' or direction == 'r':
                passX1 = uncCor
                passX2 = uncCor + 1
                passY1 = max(cCor, y1)
                passY2 = min(cCor + dim, y2)
                doorWidth = min(doorWidth, passY2 - passY1)
                self.dungeonInfo["doors"][roomNum] = \
                        {"dir":'v', "x":passX1, "y":passY1, "w":doorWidth}
            elif direction == 'u' or direction == 'd':
                passY1 = uncCor
                passY2 = uncCor + 1
                passX1 = max(cCor, x1)
                passX2 = min(cCor + dim, x2)
                doorWidth = min(doorWidth, passX2 - passX1)
                self.dungeonInfo["doors"][roomNum] = \
                        {"dir":'h', "x":passX1, "y":passY1, "w":doorWidth}

            for x in xrange(passX1, passX2):
                for y in xrange(passY1, passY2):
                    if self.dungeon.grid[y][x] == GridEnum.WALL:
                        if doorWidth != 0:
                            self.dungeon.grid[y][x] = GridEnum.DOOR
                            doorWidth -= 1
                        else:
                            self.dungeon.grid[y][x] = GridEnum.WALL

    def outputDungeon(self):
        f = open("dungeonInfo.json", 'w')
        f.write(str(json.dumps(self.dungeonInfo)))
        #for y in xrange(0, self.dungeon.height):
            #s = ""
            #for x in xrange(0, self.dungeon.width):
                #s += str(self.dungeon.grid[y][x]) + " "
            #s = s.strip() + "\n"
            #f.write(s)
            
if __name__ == "__main__":
    randDung = RandDungGen("dungeonParamText")
    randDung.outputDungeon()

