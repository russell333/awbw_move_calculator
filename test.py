from src.utils import AttributeDict
from src.awbw import findUnitsInRangeOf, getMovementTiles, findTerrainCost, \
checkTargetTile, checkCargo, loopNeighbors, checkLanding, findBuildOptions, findLandingTiles

def test():
    client_obj = AttributeDict.from_json_file('testingClientObjs.json')        
    base_damage_values= AttributeDict.from_json_file('assets/baseDamageValues.json')
    
    # Test findUnitsInRangeOf
    # test direct unit, fighter at (12, 15)
    fighterID = 78906490
    fighterHitX, fighterHitY = 16, 12 # 2 targets in range
    fighterMissX, fighterMissY = 16, 10 # no targets in range
    # test indirect unit, Carrier at (19, 12)
    carrierID = 78906455
    carrierHitX, carrierHitY = 19, 12 # two targets in range
    carrierMissX, carrierMissY = 24, 21 # out of range
    # stealth at 12, 16
    stealthID = 78906187
    stealthX, stealthY = 16, 18
    
    fighterObj = client_obj.units[fighterID]
    carrierObj = client_obj.units[carrierID]
    stealthObj = client_obj.units[stealthID]


    fighterHitUnits = findUnitsInRangeOf(fighterHitX,fighterHitY, fighterObj, client_obj, base_damage_values)
    #print (fighterHitUnits) # verified successful
    fighterMissUnits = findUnitsInRangeOf(fighterMissX,fighterMissY, fighterObj, client_obj, base_damage_values)
    #print (fighterMissUnits) # verified successful
    carrierHitUnits = findUnitsInRangeOf(carrierHitX, carrierHitY, carrierObj, client_obj, base_damage_values)
    #print (carrierHitUnits) # verified successful
    carrierMissUnits = findUnitsInRangeOf(carrierMissX, carrierMissY, carrierObj, client_obj, base_damage_values)
    #print (carrierMissUnits) # verified successful

    # Test no ammo, no secondary weapon condition
    emptyMissileID = 77405373
    missileX, missileY = 18, 15
    missileObj = client_obj.units[emptyMissileID]
    emptyMissileStrike = findUnitsInRangeOf(missileX, missileY, missileObj, client_obj, base_damage_values)
    #print (emptyMissileStrike) # verified successful
    # Test submerged sub/stealth condition with carrier moved to 16, 15
    carrierHitSubmergedStealth = findUnitsInRangeOf(16, 15, carrierObj, client_obj, base_damage_values)
    # print (carrierHitSubmergedStealth) verified successful
    # Test attacking pipe seam
    stealthHitSeam = findUnitsInRangeOf(stealthX, stealthY, stealthObj, client_obj, base_damage_values)
    #print (stealthHitSeam) # verified successful


    # Test getMovementTiles
    unit = carrierObj
    maxX = client_obj.game["max_tiles_x"] + 1 # dimensions of map
    maxY = client_obj.game["max_tiles_y"] + 1
    mType = unit["units_movement_type"]

    # mp is either max movement spaces or fuel, whichever is smaller
    maxMove = unit["units_movement_points"]
    fuel = unit["units_fuel"]
    mp = min(fuel, maxMove)
    startTile = {"x": unit["units_x"] , "y": unit["units_y"]}
    #player = unit["units_players_id"]
    unitTeam = unit["units_players_id"]  # might need to change this for multiplayer
    realCOname = client_obj.players[unitTeam]["co_name"]
    playersCOPowerOn = client_obj.players[unitTeam]["players_co_power_on"]
    playerInfo = {"co_name": realCOname, "players_co_power_on": playersCOPowerOn}
    clientObjs = client_obj

    movementTiles = getMovementTiles(maxX, maxY, mType, mp, startTile, unitTeam, playerInfo, clientObjs)
    #print (movementTiles) # seems to work for 3 examples

    # test findTerrainCosts
    #movementCost = findTerrainCost(maxX, maxY, mType, x, y, unitTeam, playerInfo, clientObjs)
    #print(movementCost) # seems to work okay?
    
    # test checkCargo
    loadableAPC = client_obj.units[78905563]
    fullAPC = client_obj.units[78905287]
    topMiddleAPC = client_obj.units[78905524]
    nearbyInfantry = client_obj.units[78905489]
    bbInSea = client_obj.units[78905589]
    lowerRightBBoat = client_obj.units[78905582]
    cappingInf = client_obj.units[77405372]
    infLoadedInBB = client_obj.units[78905628]
    joinableMega = client_obj.units[79048431]
    blackBomb = client_obj.units[78906211]
    #cargoCheck = checkCargo(transportUnit, cargoUnit)
    cargoCheck = checkCargo(bbInSea, nearbyInfantry)
    #print (cargoCheck) #seems to work

    # test checkLanding
    landingCheck = checkLanding(infLoadedInBB, bbInSea, 1, 3, clientObjs)
    #print (landingCheck) # seems to work

    # test findBuildOptions
    # NEED TO CHECK LAB AND BAN LOGIC
    findBuildOptionsOutput = findBuildOptions(8, 10, client_obj)
    #print(findBuildOptionsOutput)

    # test loopNeighbors
    neighborLoop = loopNeighbors(17, 13, carrierObj, client_obj)
    #print (neighborLoop) # seems to work fine



    # test check target tile
    targetTileOutput = checkTargetTile(blackBomb, 12, 5, clientObjs, base_damage_values)
    print (targetTileOutput)

    '''
    #print(f"Unit ids present: {client_obj.units.keys}")
    
    # Pick a unit
    testUnitID = 77164577 # inf at (3, 0)
    transportUnitID = 78487049 # loaded APC at (15, 7)
    cargoUnitID = 77164715 # the loaded infantry
    #testUnitID = 78487048 # APC at (10, 6)
    #testUnitID = 78486594 # stealth at 1, 11 (uncloaked)

    unit = client_obj.units[testUnitID]
    transportUnit = client_obj.units[transportUnitID]
    cargoUnit = client_obj.units[cargoUnitID]
    # assert it's attacking a from square adjacent to 2 enemy infantry
    x = 8
    y = 10

    #print(client_obj.buildings.keys)
    #print(6 in client_obj.buildings)
    units_in_range = findUnitsInRangeOf(x,y,unit,client_obj, base_damage_values)
    #print(units_in_range)


    # test getMovementTiles
    #print (cleintObjs["game"]["max_tiles_x"])
    maxX = client_obj.game["max_tiles_x"]
    maxY = client_obj.game["max_tiles_y"]
    mType = unit["units_movement_type"]

    # mp is either max movement spaces or fuel, whichever is smaller
    maxMove = unit["units_movement_points"]
    fuel = unit["units_fuel"]
    mp = min(fuel, maxMove)
    startTile = {"x": unit["units_x"] , "y": unit["units_y"]}
    #player = unit["units_players_id"]
    unitTeam = unit["units_players_id"]  # might need to change this for multiplayer
    realCOname = client_obj.players[859351]["co_name"]
    playersCOPowerOn = client_obj.players[859351]["players_co_power_on"]
    playerInfo = {"co_name": realCOname, "players_co_power_on": playersCOPowerOn}
    clientObjs = client_obj
    
    #getMovementTiles(maxX, maxY, mType, mp, startTile, unitTeam, playerInfo, clientObjs)

    

    # test check target tile
    #checkTargetTile(unit, x, y, clientObjs)

    # test checkCargo
    cargoCheck = checkCargo(transportUnit, cargoUnit)
    print (cargoCheck)

    # test loopNeighbors
    neighborsReturn = loopNeighbors(x, y, unit, clientObjs)
    #print (neighborsReturn)

    checkLanding(cargoUnit, transportUnit, x, y, clientObjs)

    factoryX = 11
    factoryY = 1
    buildOptions = findBuildOptions(factoryX, factoryY, clientObjs)
    #print (buildOptions)

    loadedX = 15 # location of a loaded APC
    loadedY = 7
    landingTiles = findLandingTiles(maxX, maxY, transportUnit, cargoUnit, loadedX, loadedY, clientObjs)
    print (landingTiles)'''
    return
if __name__ == "__main__":
    test()