# loop neighbors
# get own/team/enemy units around given coords

def loopNeighbors(x, y, movingUnit, clientObjs):
	playersInfo = clientObjs.players
	unitsInfo = clientObjs.units
	unitMap = clientObjs.unit_map
	viewerPId = clientObjs.viewerPId

	xv = [-1, 1, 0, 0]
	yv = [0, 0, -1, 1]
	neighbors = {"allied":[], "enemy":[], "team":[]}

	
	# If a unit is given, take it's coordinates
 	# Otherwise take the coordinates given as parameters

	if movingUnit and movingUnit["units_x"]:
 		unitX = movingUnit["units_x"]
	else: 
 		unitX = ""
	if movingUnit and movingUnit["units_y"]:
 		unitY = movingUnit["units_y"]
	else: 
 		unitY = ""

	startX = unitX if unitX else x
	startY = unitY if unitY else y
	if playersInfo[viewerPId]: viewerTeam = playersInfo[viewerPId]["players_team"]
	else: viewerTeam = playersInfo[viewerPId]

	# assigns ally/enemy/team buggily when you're viewing the opponent's options
	for i in range(4):
		ax = x + xv[i]
		ay = y + yv[i]
		if ax in unitMap and ay in unitMap[ax]:
			unitId = unitMap[ax][ay]["units_id"]
			unit = unitsInfo[unitId]
		else:
			unitId = None
			unit = None
		if unit:
			unitTeam = playersInfo[unit["units_players_id"]]["players_team"]
			if unitId and unit["units_players_id"] == viewerPId:

				# Don't add moving unit to own units
				if ax == startX and ay == startY: 
					pass
				else: neighbors["allied"].append(unit)
			#if unitId and (unitTeam == viewerTeam or grantedVisions.includes(unitTeam)):
			#	neighbors["team"].append(unit)
			if unitTeam != viewerTeam:
				neighbors["enemy"].append(unit)

	return neighbors

'''
function loopNeighbours(x, y, movingUnit, clientObjs) {
  const { 
    players: playersInfo, 
    units: unitsInfo, 
    unit_map: unitMap, 
    viewerPId 
  } = clientObjs;

  const xv = [-1, 1, 0, 0];
  const yv = [0, 0, -1, 1];
  const neighbours = {
    allied: [],
    enemy: [],
    team: []
  }

  //If a unit is given, take it's coordinates
  //Otherwise take the coordinates given as parameters
  const unitX = (movingUnit && movingUnit.units_x !== null) ? movingUnit.units_x : null;
  const unitY = (movingUnit && movingUnit.units_y !== null) ? movingUnit.units_y : null;

  const startX = unitX !== null ? unitX : x;
  const startY = unitY !== null ? unitY : y;
  const viewerTeam = playersInfo[viewerPId] && playersInfo[viewerPId].players_team;

  for(let i = 0; i < 4; i++) {
    const ax = x + xv[i];
    const ay = y + yv[i];
    const unitId = unitMap[ax] && unitMap[ax][ay] ? unitMap[ax][ay].units_id : null;
    const unit = unitsInfo[unitId];
    if(unit) {
      const unitTeam = playersInfo[unit.units_players_id].players_team;

      if(unitId && unit.units_players_id === viewerPId) {
        //Don't add moving unit to own units
        if(ax === startX && ay === startY) {

        } else {
          neighbours.allied.push(unit);
        }
      } 
      if(unitId && (unitTeam === viewerTeam || grantedVisions.includes(unitTeam))) {
        neighbours.team.push(unit);
      }
      if(unitTeam !== viewerTeam) {
        neighbours.enemy.push(unit);
      }
    }
  }
  return neighbours;
}'''