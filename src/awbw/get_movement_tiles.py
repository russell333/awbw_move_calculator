'''  
  maxX, maxY: number of tiles for each row/column (Starts at 0, so have to add 1),
  mp: unit's movement points OR fuel remaining

  unitTeam: For no team games, the team is the playerId. Otherwise "A", "B", etc,

  playerInfo: {
    co_name: ...,
    players_co_power_on: "N" / "Y" / "S"
  }
  (playerInfo object is used to find the terrain cost of given tile in findTerrainCost)
'''
import json
from queue import PriorityQueue
import queue
import heapq
from math import inf
from ..utils import AttributeDict
from .find_terrain_cost import findTerrainCost

def getMovementTiles(maxX, maxY, mType, mp, startTile, unitTeam, playerInfo, clientObjs):
  
  xv = [-1, 1, 0, 0]
  yv = [0, 0, -1, 1]
  nNodes = maxX * maxY
  visited = []

  #The total distance from the start tile, for each possible tile
  dist = []

  #Tracks where each tile comes from 
  previous = []

  #Total movement cost for each tile
  mCost = []

  for i in range(nNodes):
    visited.append(False)
    dist.append(inf)  # caution, maybe buggy!!!
    previous.append(0) # null
    mCost.append(0)   # null

  startNode = startTile["y"] * maxX + startTile["x"]
  dist[startNode] = 0

  verif = {}
  initial = {"index":startNode, "dist": 0, "x": startTile["x"], "y": startTile["y"] }
  #heap = []
  #heapq.heappush(heap, initial)
  #print (heap)
  q = PriorityQueue()
  q.put((initial["index"], initial["dist"], initial))
  tilesToDraw = [initial]
  verif[startNode] = 0
  #print(q.get())

  while not q.empty():
    #print ("Got inside while loop")
    #current = heapq.heappop(heap)
    #print (q)
    current = q.get()
    #print (current)
    index = current[2]["index"]
    minValue = current[2]["dist"]
    x = current[2]["x"]
    y = current[2]["y"]

    visited[index] = True
    verif.clear() #hopefully this has the same effect as "delete verif"

    if dist[index] < minValue:
      continue

    for i in range(4):
      ax = x + xv[i]
      ay = y + yv[i]

      terrainCost = findTerrainCost(maxX, maxY, mType, ax, ay, unitTeam, playerInfo, clientObjs)
      #terrainCost = 1

      #Tile is outside of the map, or unit can't move to given tile
      if ax < 0 or ay < 0 or ax >= maxX or ay >= maxY or not terrainCost:
        continue

      nextNodeIndex = ay * maxX + ax
      mCost[nextNodeIndex] = terrainCost
      #print ("GOT INSIDE FOR LOOP")
      if(visited[nextNodeIndex]):
        continue

      if terrainCost == "A" and nextNodeIndex not in verif:
      # Mark previous tile where the attack is made from and skip to next iteration
        previous[nextNodeIndex] = index
        verif[nextNodeIndex] = "A"
        continue

      newDist = minValue + terrainCost

      if newDist < dist[nextNodeIndex] and newDist < mp:
        previous[nextNodeIndex] = index
        dist[nextNodeIndex] = newDist
        #print("inner if loop")

        if nextNodeIndex not in verif:
          #queueTiles.put({"index": nextNodeIndex, "dist": newDist, "x":ax, "y":ay})
          #heapq.heappush(heap, {"index": nextNodeIndex, "dist": newDist, "x":ax, "y":ay})
          q.put((nextNodeIndex, newDist, {"index": nextNodeIndex, "dist": newDist, "x":ax, "y":ay}))
          verif[nextNodeIndex] = newDist
          tilesToDraw.append({"index": nextNodeIndex, "x":ax, "y":ay})
        else:
          for node in q:
            print ("jank thing ran")
            if node[2]["index"] == nextNodeIndex:
              node[1] = newDist
              node[2]["dist"] = newDist

  #print("got movement tile to run")
  movementInfo = {"dist": dist, "previous": previous, "mCost": mCost, "mp":mp}
  #print(movementInfo)
  return movementInfo
'''/* 
  maxX, maxY: number of tiles for each row/column (Starts at 0, so have to add 1),
  mp: unit's movement points OR fuel remaining

  unitTeam: For no team games, the team is the playerId. Otherwise "A", "B", etc,

  playerInfo: {
    co_name: ...,
    players_co_power_on: "N" / "Y" / "S"
  }
  (playerInfo object is used to find the terrain cost of given tile in findTerrainCost)

*/
function getMovementTiles(maxX, maxY, mType, mp, startTile, unitTeam, playerInfo, clientObjs) {
  const xv = [-1, 1, 0, 0];
  const yv = [0, 0, -1, 1];
  const nNodes = maxX * maxY;
  const visited = [];

  //The total distance from the start tile, for each possible tile
  const dist = [];

  //Tracks where each tile comes from 
  const previous = [];

  //Total movement cost for each tile
  const mCost = [];

  for(let i = 0; i < nNodes; i++) {
    visited.push(false);
    dist.push(Infinity);
    previous.push(null);
    mCost.push(null);
  }
  const startNode = startTile.y * maxX + startTile.x;
  dist[startNode] = 0;

  //TinyQueue script needs to be included
  const queue = new TinyQueue([], function(a, b) {
    return a.dist - b.dist;
  });

  //Verification object to not include a tile twice
  const verif = {};
  const initial = {index: startNode, dist: 0, x: startTile.x, y: startTile.y};
  queue.push(initial);

  const tilesToDraw = [initial];
  verif[startNode] = 0;

  while(queue.length != 0) {
    const current = queue.pop();
    const index = current.index;
    const minValue = current.dist;
    const x = current.x;
    const y = current.y;

    visited[index] = true;
    delete verif[index];

    if(dist[index] < minValue) continue;

    for(let i = 0; i < 4; i++) {
      const ax = x + xv[i];
      const ay = y + yv[i];

      const terrainCost = findTerrainCost(mType, ax, ay, unitTeam, playerInfo, clientObjs);
      
      //Tile is outside of the map, or unit can't move to given tile
      if(ax < 0 || ay < 0 || ax >= maxX || ay >= maxY || !terrainCost) continue;
      
      const nextNodeIndex = ay * maxX + ax;
      mCost[nextNodeIndex] = terrainCost;

      if(visited[nextNodeIndex]) continue;

      if(terrainCost === "A" && !verif[nextNodeIndex]) {
        //Mark previous tile where the attack is made from and skip to next iteration
        previous[nextNodeIndex] = index;
        verif[nextNodeIndex] = "A";
        continue;
      }

      const newDist = minValue + terrainCost;

      if(newDist < dist[nextNodeIndex] && newDist <= mp) {
        previous[nextNodeIndex] = index;
        dist[nextNodeIndex] = newDist;

        if(!verif[nextNodeIndex]) {
          queue.push({index: nextNodeIndex, dist: newDist, x: ax, y: ay});
          verif[nextNodeIndex] = newDist;
          tilesToDraw.push({index: nextNodeIndex, x: ax, y: ay});
        } 
        else {
          for(const node in queue) {
            if(queue[node].index == nextNodeIndex) queue[node].dist = newDist;
          }
        }
      }
    }
  }

  const movementInfo = {
    dist: dist,
    previous: previous,
    mCost: mCost,
    mp: mp
  }
  
  return movementInfo;

}'''