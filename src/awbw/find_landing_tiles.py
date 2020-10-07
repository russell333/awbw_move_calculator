# find which tiles loaded units can unload to from given transport
from .find_terrain_cost import findTerrainCost
def findLandingTiles(maxX, maxY, transportUnit, loadedUnit, x, y, clientObjs):
	playersInfo = clientObjs.players
	unitMap = clientObjs.unit_map

	player = playersInfo[transportUnit["units_players_id"]]
	unitTeam = player["players_team"]

	loadedUnitMType = loadedUnit["units_movement_type"]

	xv = [-1, 1, 0, 0]
	yv = [0, 0, -1, 1]
	landingTiles = []

	# Loop adjacent tiles to transport
	for i in range(4):
		ax = x + xv[i]
		ay = y + yv[i]

		loadedUnitMCost = findTerrainCost(maxX, maxY, loadedUnitMType, ax, ay, unitTeam, player, clientObjs)

		# Skip if loaded unit has no terrain cost on landing terrain, 
		# or there is possible attack
		if not loadedUnitMCost or loadedUnit == "A": continue
		transportUnitId = transportUnit["units_id"]
		if ax in unitMap and ay in unitMap[ax] and "units_id" in unitMap[ax][ay]:
			adjacentUnitId = unitMap[ax][ay]["units_id"]
		else: adjacentUnitId = ""

 	 	# Skip if there is a unit adjacent to the end of the path and the 
 	 	# unit is not itself, since the unit hasn't actually moved yet 
 	   	# when the option appears
		if adjacentUnitId and adjacentUnitId != transportUnit: continue

		landingTiles.append({x: ax, y: ay})
	return landingTiles

'''
//find which tiles loaded units can unload to from given transport
function findLandingTiles(transportUnit, loadedUnit, x, y, clientObjs) {
  const { players: playersInfo, unit_map: unitMap } = clientObjs;

  const player = playersInfo[transportUnit.units_players_id];
  const unitTeam = player.players_team;

  const loadedUnitMType = loadedUnit.units_movement_type;
  
  const xv = [-1, 1, 0, 0];
  const yv = [0, 0, -1, 1];
  const landingTiles = [];

  //Loop adjacent tiles to transport
  for(let i = 0; i < 4; i++) {
    const ax = x + xv[i];
    const ay = y + yv[i];

    const loadedUnitMCost = findTerrainCost(loadedUnitMType, ax, ay, unitTeam, player, clientObjs);

    //Skip if loaded unit has no terrain cost on landing terrain, or there is possible attack
    if(!loadedUnitMCost || loadedUnitMCost === "A") continue;
    const transportUnitId = transportUnit.units_id;
    const adjacentUnitId = unitMap[ax] && unitMap[ax][ay] && unitMap[ax][ay].units_id;

    //Skip if there is a unit adjacent to the end of the path and the unit is not itself
    //Since the unit hasn't actually moved yet when the option appears
    if(adjacentUnitId && adjacentUnitId !== transportUnitId) continue;
    
    landingTiles.push({x: ax, y: ay});

  }
  return landingTiles;
}
'''