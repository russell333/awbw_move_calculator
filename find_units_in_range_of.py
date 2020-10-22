#Find units that are in attack range of given unit
#Used to draw clickable attack squares

# TODO: Decompose the giant function here into modular helper functions

import json
from ..utils import AttributeDict

def findUnitsInRangeOf(x, y, selectedUnit, clientObj, baseDamageValues):
    
    playersInfo = clientObj.players
    buildingsInfo = clientObj.buildings
    genericUnits = clientObj.generic_units
    unitsInfo = clientObj.units
    unitMap = clientObj.unit_map
    
    maxRange = selectedUnit.units_long_range
    minRange = selectedUnit.units_short_range
    
    selectedUnitTeam = playersInfo[selectedUnit.units_players_id].players_team
    
    # Increment range by 1 for direct units
    if minRange <= 0:
        minRange = 1
        maxRange = 1
        
    attAmmo = selectedUnit.units_ammo
    attName = selectedUnit.units_name
    attGenId = genericUnits[selectedUnit.units_name].units_id;
    
    unitsInRange = []
    for i in range(-maxRange, maxRange+1):
        for j in range(-maxRange, maxRange+1):
            absoluteSum = abs(i) + abs(j)
            if (absoluteSum <= maxRange and absoluteSum >= minRange):
                # Tile within range of attacker
                ax = x + i
                ay = y + j
                
                if ax in buildingsInfo and ay in buildingsInfo[ax]:
                    terrainName = buildingsInfo[ax][ay].terrain_name
                else:
                    terrainName = None
                    
                ATTACK1 = baseDamageValues.ATTACK1
                ATTACK2 = baseDamageValues.ATTACK2
                
                # If there is a unit and pipe seam on the same tile, only consider the unit
                
                # Enemy unit exists on selected square
                if ax in unitMap and ay in unitMap[ax]:
                    unitId = unitMap[ax][ay].units_id
                    unit = unitsInfo[unitId]
                    defGenId = genericUnits[unit.units_name].units_id
                   
                    # Skip attackers that can't attack the defender
                    if not (attGenId in ATTACK1 and defGenId in ATTACK1[attGenId]) \
                        and not (attGenId in ATTACK2 and defGenId in ATTACK2[attGenId]):
                            continue
                    # Skip attackers with no ammo and no secondary attack
                    if (attGenId in ATTACK1 and defGenId in ATTACK1[attGenId] and attAmmo == 0) \
                        and not (attGenId in ATTACK2 and defGenId in ATTACK2[attGenId]):
                            continue
                    # Skip attacking units on the same team
                    if unitMap[ax][ay]["team"] == selectedUnitTeam: continue
                    
                    # Exclude hidden units that can't be attacked
                    defName = unit.units_name 
                    subDive = unit.units_sub_dive
                    defHidden = (subDive == 'Y' or subDive == 'D')
                    if defHidden and defName == 'Stealth' and attName not in ['Stealth', 'Fighter']:
                        continue
                    if defHidden and defName == 'Sub' and attName not in ['Cruiser', 'Sub']:
                        continue
                    unitsInRange.append(unitsInfo[unitId])
                
                # Terrain in range is pipe seam, use neotank as defender
                elif terrainName is not None and 'seam' in terrainName.lower():
                    defGenId = genericUnits.Neotank.units_id
                    # Skip attackers that can't attack the defender
                    if not (attGenId in ATTACK1 and defGenId in ATTACK1[attGenId]) \
                        and not (attGenId in ATTACK2 and defGenId in ATTACK2[attGenId]):
                            continue
                    # Skip attackers with no ammo and no secondary attack
                    if (attGenId in ATTACK1 and defGenId in ATTACK1[attGenId] and attAmmo == 0) \
                        and not (attGenId in ATTACK2 and defGenId in ATTACK2[attGenId]):
                            continue    
                    
                    unit = {
                        'units_id': buildingsInfo[ax][ay].buildings_id,
                        'units_name': 'Pipe Seam',
                        'units_x': ax,
                        'units_y': ay
                    }
                    unitsInRange.append(AttributeDict(unit))
    return unitsInRange           
    '''
    let maxRange = selectedUnit.units_long_range;
    let minRange = selectedUnit.units_short_range;
    
    const selectedUnitTeam = playersInfo[selectedUnit.units_players_id].players_team;
    
    //Increment range by 1 for direct units for the loop
    if(minRange <= 0) {
      minRange = 1;
      maxRange = 1;
    }
    
    const attAmmo = selectedUnit.units_ammo;
    const attName = selectedUnit.units_name;
    const attGenId = genericUnits[selectedUnit.units_name].units_id;
    
    const unitsInRange = [];
    
    for(let i = -maxRange; i <= maxRange; i++) {
      for(let j = -maxRange; j <= maxRange; j++) {
        const absoluteSum = Math.abs(i) + Math.abs(j);
    
        if(absoluteSum <= maxRange && absoluteSum >= minRange) {
    
          const ax = x + i;
          const ay = y + j;
    
          //Needed for pipeseams. Pipeseams are stored in buildingsInfo
          const terrainName = buildingsInfo[ax] && buildingsInfo[ax][ay] && buildingsInfo[ax][ay].terrain_name
    
          const ATTACK1 = baseDamageValues.ATTACK1;
          const ATTACK2 = baseDamageValues.ATTACK2;
    
          //If there is a unit and a pipe seam on the same tile, only add the unit
    
          //Enemy unit is in range
          if(unitMap[ax] && unitMap[ax][ay] && unitMap[ax][ay].team !== selectedUnitTeam) {
            const unitId = unitMap[ax][ay].units_id;
            const unit = unitsInfo[unitId];
            const defGenId = genericUnits[unit.units_name].units_id;
    
            if(!(ATTACK1[attGenId] && ATTACK1[attGenId][defGenId]) && !(ATTACK2[attGenId] && ATTACK2[attGenId][defGenId])) continue;
        
            //Skip out of ammos with no secondary attack
            if((ATTACK1[attGenId] && ATTACK1[attGenId][defGenId] && attAmmo === 0) && !(ATTACK2[attGenId] && ATTACK2[attGenId][defGenId])) continue;
    
            //Exclude hidden units that can't be attacked by certain units
            const defName = unit.units_name;
            const subDive = unit.units_sub_dive;
            const defHidden = subDive === "Y" || subDive === "D";
    
            if(defHidden && defName === "Stealth" && attName !== "Stealth" && attName !== "Fighter") continue;
            
            if(defHidden && defName === "Sub" && attName !== "Cruiser" && attName !== "Sub") continue;
    
            unitsInRange.push(unitsInfo[unitId]);
          }
    
          //Terrain in range is pipe seam
          //Use Neotank as defender
          else if(/Seam/.test(terrainName)) {
            const defGenId = genericUnits["Neotank"].units_id;
    
            if(!(ATTACK1[attGenId] && ATTACK1[attGenId][defGenId]) && !(ATTACK2[attGenId] && ATTACK2[attGenId][defGenId])) continue;
    
            //Skip out of ammos with no secondary attack
            if((ATTACK1[attGenId] && ATTACK1[attGenId][defGenId] && attAmmo === 0) && !(ATTACK2[attGenId] && ATTACK2[attGenId][defGenId])) continue;
      
            unitsInRange.push({ 
              units_id: buildingsInfo[ax][ay].buildings_id,
              units_name: "Pipe Seam", 
              units_x: ax, 
              units_y: ay 
            });
          }
        }
      }
    }
    return unitsInRange; '''
