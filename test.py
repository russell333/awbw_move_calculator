# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 21:45:24 2020

@author: Daniel Tan
"""


from src.utils import AttributeDict
from src.awbw import findUnitsInRangeOf, getMovementTiles, findTerrainCost, \
checkTargetTile, checkCargo, loopNeighbors, checkLanding, findBuildOptions, findLandingTiles

def test():
    client_obj = AttributeDict.from_json_file('clientObj.json')        
    base_damage_values= AttributeDict.from_json_file('assets/baseDamageValues.json')
    
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

    # test findTerrainCosts
    movementCost = findTerrainCost(maxX, maxY, mType, x, y, unitTeam, playerInfo, clientObjs)
    #print(movementCost)

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
    print (landingTiles)
if __name__ == "__main__":
    test()