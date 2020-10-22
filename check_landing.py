# //Check if transport unit is on a tile where it can unload
def checkLanding(cargoUnit, transportUnit, x, y, clientObjs):
	buildingsInfo = clientObjs.buildings
	terrainInfo = clientObjs.terrain

	terrainName = None
	if x in terrainInfo and y in terrainInfo[x] and "terrain_name" in terrainInfo[x][y]:
		terrainName = terrainInfo[x][y]["terrain_name"]
	elif x in buildingsInfo and y in buildingsInfo[x] and "terrain_name" in buildingsInfo[x][y]:
		terrainName = buildingsInfo[x][y]["terrain_name"]

	if not terrainName: return
	if not cargoUnit: return

	transportName = transportUnit["units_name"]
	# Landers and black boats can unload anywhere except sea/reef
	if (transportName == "T-Copter" or transportName == "Lander" or \
		transportName == "Black Boat"):
		if  ("Sea" in terrainName):
			return False
		elif ("Reef" in terrainName):
			return False
		else: return True
	elif transportName == "APC" or transportName == "Cruiser" or transportName == "Carrier":
		return True