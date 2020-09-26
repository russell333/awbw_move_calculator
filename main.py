# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 21:45:24 2020

@author: Daniel Tan
"""


from src.utils import AttributeDict
from src.awbw import findUnitsInRangeOf, getMovementTiles, findTerrainCost

def main():
    client_obj = AttributeDict.from_json_file('clientObj.json')        
    base_damage_values= AttributeDict.from_json_file('assets/baseDamageValues.json')
    
    print(f"Unit ids present: {client_obj.units.keys}")
    
    # Arbitrarily pick a unit
    testUnitID = 77164577
    unit = client_obj.units[testUnitID]
    # assert it's attacking a from square adjacent to 2 enemy infantry
    x = 8
    y = 10
    
    #print(client_obj.buildings.keys)
    #print(6 in client_obj.buildings)
    units_in_range = findUnitsInRangeOf(x,y,unit,client_obj, base_damage_values)
    print(units_in_range)


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
    player = unit["units_players_id"]
    unitTeam = unit["units_players_id"]  # might need to change this for multiplayer
    realCOname = client_obj.players[859351]["co_name"]
    playersCOPowerOn = client_obj.players[859351]["players_co_power_on"]
    playerInfo = {"co_name": realCOname, "players_co_power_on": playersCOPowerOn}
    clientObjs = client_obj
    
    getMovementTiles(maxX, maxY, mType, mp, startTile, unitTeam, playerInfo, clientObjs)

    # test findTerrainCosts
    findTerrainCost(mType, x, y, unitTeam, player, clientObjs)


    
if __name__ == "__main__":
    main()