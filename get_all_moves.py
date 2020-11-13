from src.utils import AttributeDict
from src.awbw import getMovementTiles, findBuildOptions, checkTargetTile, loopNeighbors, findLandingTiles

# Returns a list of movement encodings. See below for encoding syntax.
# NOTE: does not allow for CO swap at end of turn
def getAllMoves():
	client_obj = AttributeDict.from_json_file('testingClientObjs.json')        
	unitDict = client_obj.units
	viewerPId = client_obj.viewerPId
	base_damage_values= AttributeDict.from_json_file('assets/baseDamageValues.json')

	maxX = client_obj.game["max_tiles_x"] + 1
	maxY = client_obj.game["max_tiles_y"] + 1

	# syntax: 20, 20 Wait at 19, 20: 2020W1920
	# 20, 21 unload unit 2 at 12, 13 to 12, 14: 2021U212141213
	# 13, 4 move to 14, 3 and attack 14, 4: 1304F14041403
	allMoves = []

	# loop over all unit moves
	for unitID in unitDict.keys:
		unit = unitDict[unitID]
		unitTeam = unit["units_players_id"]
		unitX = unit["units_x"]
		unitY = unit["units_y"]
		#print (unitX)
		if unitTeam == viewerPId:
			# get tiles it can move to
			mType = unit["units_movement_type"]
			maxMove = unit["units_movement_points"]
			fuel = unit["units_fuel"]
			# mp is either max movement spaces or fuel, whichever is smaller
			mp = min(fuel, maxMove)
			startTile = {"x": unit["units_x"] , "y": unit["units_y"]}
			realCOname = client_obj.players[unitTeam]["co_name"]
			playersCOPowerOn = client_obj.players[unitTeam]["players_co_power_on"]

			playerInfo = {"co_name": realCOname, "players_co_power_on": playersCOPowerOn}

			movementInfo = getMovementTiles(maxX, maxY, mType, mp, startTile, unitTeam, playerInfo, client_obj)
			mCost = movementInfo["mCost"]
			for index in range(len(mCost)):
				if mCost[index] != 0:
					# convert index = x*maxX + y to (x, y)
					x = index%maxX
					y = index//maxX
					options = checkTargetTile(unit, x, y, client_obj, base_damage_values)
					if options:
						for option in options:
							# starting tile 
							# make single digit nums double digits
							if len(str(unitX)) == 1: unitX = "0" + str(unitX)
							if len(str(unitY)) == 1: unitY = "0" + str(unitY)
							actionString = str(unitX) + str(unitY)

							# ending tile (comes at end of action string)
							destinationX = x
							destinationY = y
							if len(str(destinationX)) == 1: destinationX = "0" + str(destinationX)
							if len(str(destinationY)) == 1: destinationY = "0" + str(destinationY)
							endofString = str(destinationX) + str(destinationY)

							# special cases for including multiple actions mapped to "option" array
							if option["option"] == "Fire":
								neighbors = loopNeighbors(x, y, unit, client_obj)
								for enemy in neighbors["enemy"]:
									targetX, targetY  = enemy["units_x"], enemy["units_y"]
									if len(str(targetX)) == 1: targetX = "0" + str(targetX)
									if len(str(targetY)) == 1: targetY = "0" + str(targetY)
									fireString = actionString + "F" + str(targetX) + str(targetY) + endofString
									allMoves.append(fireString)
							# Note there is no $ check on the Repair action
							if option["option"] == "Repair":
								neighbors = loopNeighbors(x, y, unit, client_obj)

								for ally in neighbors["allied"]:
									targetX, targetY  = ally["units_x"], ally["units_y"]
									if len(str(targetX)) == 1: targetX = "0" + str(targetX)
									if len(str(targetY)) == 1: targetY = "0" + str(targetY)
									repairString = actionString + "R" + str(targetX) + str(targetY) + endofString
									allMoves.append(repairString)
							
							# 20, 21 unload unit 2 at 12, 13 to 12, 14: 2021U212141213
							# only counts in-place drops
							if option["option"] == "Unload":
								if unit['units_cargo1_units_id']:
									cargoUnit = unitDict[unit['units_cargo1_units_id']]
									landingTiles = findLandingTiles(maxX, maxY, unit, cargoUnit, x, y, client_obj)
									for landing in landingTiles:
										dropX, dropY = landing[x], landing[y]
										if len(str(dropX)) == 1: targetX = "0" + str(dropX)
										if len(str(dropY)) == 1: targetY = "0" + str(dropY)
										unloadString = actionString + "D" + "1" + str(targetX) + str(targetY) + endofString
										#print (unloadString)
										allMoves.append(unloadString)
								if unit['units_cargo2_units_id']:
									cargoUnit = unitDict[unit['units_cargo2_units_id']]
									landingTiles = findLandingTiles(maxX, maxY, unit, cargoUnit, x, y, client_obj)
									#print (landingTiles)
									for landing in landingTiles:
										dropX, dropY = landing[x], landing[y]
										if len(str(dropX)) == 1: targetX = "0" + str(dropX)
										if len(str(dropY)) == 1: targetY = "0" + str(dropY)
										unloadString = actionString + "D" + "2" + str(targetX) + str(targetY) + endofString
										#print (unloadString)
										allMoves.append(unloadString)

							# This catches Load, Join, Supply, Hide/Unhide, Capt, Launch, Explode, Delte and Wait
							# for all of which there is a unique action associated with "option"
							else: 
								# append first letter of the action
								actionString += option["option"][0]
								actionString += endofString
								allMoves.append(actionString)	
								#print (actionString)
	# non-unit moves

	# Powers: COP available = "COP", SCOP available = "SCOP"
	COPMin = client_obj.players[viewerPId]["co_max_power"]
	SCOPMin = client_obj.players[viewerPId]["co_max_spower"]
	playerCharge = client_obj.players[viewerPId]["players_co_power"]
	# don't allow activate S/COP if power already active
	if client_obj.players[viewerPId]["players_co_power_on"] == "N":
		if playerCharge >= SCOPMin: 
			allMoves.append("SCOP")
			allMoves.append("COP")
		elif playerCharge >= COPMin: 
			allMoves.append("COP")


	# Build	units				
	# Syntax: build at 10, 21 a fighter is 1021BFighter	
	for x in range(maxX):
		for y in range(maxY):
			buildOptions = findBuildOptions(x, y, client_obj)
			# discount units on top of production facility
			if x in client_obj.unit_map and y in client_obj.unit_map[x]:
				continue
			# discount enemy production
			ownBuildings = client_obj.players_buildings[viewerPId]
			if x in ownBuildings and y in ownBuildings[x]:
				targetX = x
				targetY = y
				if len(str(x)) == 1: targetX = "0" + str(targetX)
				if len(str(y)) == 1: targetY = "0" + str(targetY)
				actionString = str(targetX) + str(targetY) + "B"
				if buildOptions:
					for unitName in buildOptions:
						allMoves.append(actionString + unitName)

	print (allMoves)
	return allMoves

if __name__ == "__main__":
	getAllMoves()