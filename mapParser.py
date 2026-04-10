from colored import Fore, Back, Style
import math
import roomsData
import mapRenderingDicts
import mapSet 
rooms=roomsData.rooms
roomInitialsDict=mapRenderingDicts.roomInitialsDict
roomColorDict=mapRenderingDicts.roomColorDict
vertDoorInitialDict=mapRenderingDicts.vertDoorInitialDict
horizontalDoorInitialDict=mapRenderingDicts.horizontalDoorInitialDict
mapSet=mapSet.mapSet
MAP_WIDTH=6
MAP_HEIGHT=6
HORIZONTAL_DOOR_COUNT=MAP_WIDTH-1 #per row
VERTICAL_DOOR_COUNT=MAP_WIDTH #per row
def split_string_by_n(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

def findRoomType(room):
    #finds the type of room from the room's dictionary entry
  for i in range(len(rooms)):
    if rooms[i]["roomID"]==room:
      roomType=rooms[i]["type"]
      return roomInitialsDict[roomType]
    
def findDoorType(door):
    #parse input data into readable strings 
  match door:
    case 0:
      return "normal"
    case 1:
      return "wither"
    case 2:
      return "blood"
    case 3:
      return "entrance"
    case _:
      return "none"
    
def createLinkedLists(currentMap):
  inputLIST=currentMap.split(";")
  #"F7;1704301189361;026097...;0091..." ->
  # ["F7","1704301189361","026097...","0091..."]
  #                         ^^^rooms    ^^^doors
  inputRoomLIST=inputLIST[2]
  inputDoorLIST=inputLIST[3]
  inputRoomLIST=split_string_by_n(inputRoomLIST,3)
  #"026097096005088..." -> ["026","097","096","005","088"...]
  inputDoorLIST=split_string_by_n(inputDoorLIST,1)
  #"009190901..." -> ["0","0","9","1","9","0","9","0","1"...]                                                                                                                                                                                              
  horizontalDoors=[]
  for i in range(MAP_HEIGHT):
    for j in range(MAP_WIDTH-1):
      horizontalDoors+=inputDoorLIST[i*11+j]
  #create horizontal door list eg. 009190901999099999911999992099199990900909999990990903999999->
  #['0', '0', '9', '1', '9', '9', '0', '9', '9', '9', '9', '9', '9', '9', '2', '9', '9', '0', '9',
  #'0', '9', '9', '9', '0', '9', '9', '9', '9', '9', '9']
  verticalDoors=[]
  for i in range(MAP_HEIGHT-1):
    for j in range(MAP_WIDTH):
      verticalDoors+=inputDoorLIST[(i*(VERTICAL_DOOR_COUNT+HORIZONTAL_DOOR_COUNT)+j+HORIZONTAL_DOOR_COUNT)]

  #same as horizontal door list but for vertical doors 
  deDuplicatedRoomList=[]
  for i in inputRoomLIST:
    if not(i in deDuplicatedRoomList):
      deDuplicatedRoomList+=[i]
  #room list without duplicate entries
  roomConnections=[[]]
  for i in range(len(deDuplicatedRoomList)-1):
    roomConnections+=[[]]
  for i in range(len(horizontalDoors)):
    if horizontalDoors[i]!="9":
      tempList=findAjacentRoomsH(currentMap,i)
      room1=tempList[0][0]
      room2=tempList[1][0]
      roomConnections[deDuplicatedRoomList.index(room1)]+=[room2]
      roomConnections[deDuplicatedRoomList.index(room2)]+=[room1]
  #iterates through all horizontal doors, checking if they are adjacent to two different rooms
  #if they are, it adds the rooms to each other's room connections
  for i in range(len(verticalDoors)):
    if verticalDoors[i]!="9":
      tempList=findAjacentRoomsV(currentMap,i)
      room1=tempList[0][0]
      room2=tempList[1][0]
      roomConnections[deDuplicatedRoomList.index(room1)]+=[room2]
      roomConnections[deDuplicatedRoomList.index(room2)]+=[room1]
  return [deDuplicatedRoomList,roomConnections]

def restructureTree(DDRL, RC):
  adj={}
  for i in range(len(DDRL)):
    adj[DDRL[i]]=RC[i]
  processedRooms = set(['012'])
  #creates linked list
  def getRoom(roomName):
    adjacentRooms = adj.get(roomName, [])
    childrenNodes = []
    for adjacentRoom in adjacentRooms:
      if adjacentRoom in adj and adjacentRoom not in processedRooms:
        processedRooms.add(adjacentRoom)
        childrenNodes.append(getRoom(adjacentRoom))
    return [roomName, childrenNodes]
  #constructs tree
  return getRoom('012') 
 
def findAjacentRoomsH(currentMap,doorIDH):
  inputLIST=currentMap.split(";")
  inputRoomLIST=inputLIST[2]
  inputDoorLIST=inputLIST[3]
  inputRoomLIST=split_string_by_n(inputRoomLIST,3)
  inputDoorLIST=split_string_by_n(inputDoorLIST,1)
  room1=inputRoomLIST[math.floor(doorIDH/5)+doorIDH]
  room2=inputRoomLIST[math.floor(doorIDH/5)+doorIDH+1]
  return([room1],[room2])

def findAjacentRoomsV(currentMap,doorIDV):
  inputLIST=currentMap.split(";")
  inputRoomLIST=inputLIST[2]
  inputDoorLIST=inputLIST[3]
  inputRoomLIST=split_string_by_n(inputRoomLIST,3)
  inputDoorLIST=split_string_by_n(inputDoorLIST,1)
  room1=inputRoomLIST[doorIDV]
  room2=inputRoomLIST[doorIDV+6]
  return([room1],[room2])

def outputColorPrinter(roomInitial):
  #takes room initial (eg. "N" or "P") and prints the correct color and that initial
  color=roomColorDict[roomInitial]
  print(f'{Fore.rgb(color[0],color[1],color[2])}{roomInitial}{Style.reset}',end="")
def doorPrinter(door):
  print(f'{Fore.rgb(107, 58, 17)}{door}{Style.reset}',end="")
def printMap(currentMap):
  inputLIST=currentMap.split(";")
  inputRoomLIST=inputLIST[2]
  inputDoorLIST=inputLIST[3]
  inputRoomLIST=split_string_by_n(inputRoomLIST,3)
  inputDoorLIST=split_string_by_n(inputDoorLIST,1)
  outputMapList=[]
  for i in range(len(inputRoomLIST)):
    outputMapList+=findRoomType(int(inputRoomLIST[i]))
    if i%6==5:
      continue
  horizontalRoomJoiners=[]
  for i in range(len(inputRoomLIST)):
    if i%6==0:
      continue
    else:
      if inputRoomLIST[i-1]==inputRoomLIST[i]:
        horizontalRoomJoiners+=[True]
      else:
        horizontalRoomJoiners+=[False]
  #creates a list of where joiners should be placed 
  vertRoomJoiners=[]
  for i in range(len(inputRoomLIST)):
    if i<6:
      continue
    else:
      if inputRoomLIST[i-6]==inputRoomLIST[i]:
        vertRoomJoiners+=[True]
      else:
        vertRoomJoiners+=[False]
  outputDoorList=[]
  for i in range(len(inputDoorLIST)):
    outputDoorList+=[findDoorType(int(inputDoorLIST[i]))]
  for i in range(MAP_HEIGHT):
    outputColorPrinter(outputMapList[i*6])
    for j in range(1,MAP_WIDTH):
      doorCoord=((i*(MAP_WIDTH-1))+j-1)
      if horizontalRoomJoiners[doorCoord]:
        outputColorPrinter(roomInitialsDict[findDoorType(0)])         
      else:
        doorPrinter(horizontalDoorInitialDict[outputDoorList[i*11+j-1]])
      outputColorPrinter(outputMapList[i*6+j])
    #room printer
    print("")
    if i!=MAP_HEIGHT-1:
      for j in range(MAP_WIDTH):
        if vertRoomJoiners[i*6+j]:
          outputColorPrinter(roomInitialsDict[findDoorType(0)])
        else:
          doorPrinter(vertDoorInitialDict[outputDoorList[i*11+j+5]])


        print(" ",end="")
    #door printer
    print("")

def printTree(tree, indent=0):
  #Tree debug print / initial navigation
  nodeId = tree[0]
  children = tree[1]
  prefix = "    " * indent
  print(f"{prefix}{nodeId}")
  for child in children:
    printTree(child, indent + 1)
for i in mapSet:
  printMap(i)
  print(printTree(restructureTree(createLinkedLists(i)[0],createLinkedLists(i)[1])))
printMap("F7;1704301189361;026097096005088088068018103043088088112112103103102015014014014134134077065039044130134077066066066066012077;009190901999099999911999992099199990900909999990990903999999")                                                                                                                                                                                                
#actually runs the program
tempList=createLinkedLists("F7;1704301189361;026097096005088088068018103043088088112112103103102015014014014134134077065039044130134077066066066066012077;009190901999099999911999992099199990900909999990990903999999")                                                                                                                                                                                                
tree=restructureTree(tempList[0],tempList[1])
printTree(tree)