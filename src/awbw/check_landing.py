# //Check if transport unit is on a tile where it can unload
def checkLanding(cargoUnit, transportUnit, x, y, clientObjs):
	buildingsInfo = clientObjs.buildings
	terrainInfo = clientObjs.terrain

	
	terrainName = (terrainInfo[x] and terrainInfo[x][y] and terrainInfo[x][y]["terrain_name"]) \
	or (buildingsInfo[x] and buildingsInfo[x][y] and buildingsInfo[x][y]["terain_name"])

	if not terrainName: return
	if not cargoUnit: return

	transportName = transportUnit["units_name"]

	# Landers and black boats can unload anywhere except sea/reef
	if ((transportName == "T-Copter" or transportName == "Lander" or \
		transportName == "Black Boat") and ("Sea" or "Reef" in terrainName)):
		return True
	elif transportName == "APC" or transportName == "Cruiser" or transportName == "Carrier":
		return True