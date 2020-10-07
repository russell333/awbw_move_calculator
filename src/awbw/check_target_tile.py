# Select the available options when clicking on a movement tile
def checkTargetTile(selectedUnit, x, y, clientObjs):

  buildingsInfo = clientObjs.buildings
  playersInfo = clientObjs.players
  unitsInfo = clientObjs.units
  unitMap = clientObjs.unit_map

  optionsDisplay = []
  currentCargo = selectedUnit["units_cargo1_units_id"] or selectedUnit["units_cargo2_units_id"]

  # Load option
  if x in unitMap and y in unitMap[x] and selectedUnit["units_id"] != unitMap[x][y]["units_id"]:
    targetUnitId = unitMap[x][y]["units_id"]
    targetUnit = unitsInfo[targetUnitId]
    targetName = targetUnit["units_name"]

    #canLoad = checkCargo(targetUnit, selectedUnit)
    canLoad = False
    # possibly wrong:
    targetCargo = targetUnit["units_cargo1_units_id"] or targetUnit["units_cargo2_units_id"]

    if canLoad:
      loadOption = {"option": "Load", "clickable": True}
      optionsDisplay.append(loadOption)

      # Transport is full
      if canLoad != "Y":
        loadOption["clickable"] = False
        loadOption["message"] = canLoad

      optionsDisplay.append(loadOption)


    # Join option
    if targetName == selectedUnit["units_name"] and targetUnit["units_hit_points"] < 10 \
    and not targetCargo and not currentCargo:
      return optionsDisplay

    if optionsDisplay.length() != 0: return optionsDisplay

    return # empty return statement may be a problem

  # Unload option

  #isLandingTile = checkLanding(currentCargo, selectedUnit, x, y, clientObjs)
  isLandingTile = False
  if isLandingTile and selectedUnit["units_x"] == x and selectedUnit["units_y"] == y:
    optionsDisplay.append({"option": "Unload", "clickable": True})

  # Repair option
  
  '''neighbors = loopNeighbours(x, y, selectedUnit, clientObjs)
  alliedNeighbors = neighbors.allied.length != 0

  if selectedUnit["units_name"] == "Black Boat" and alliedNeighbors:
    optionsDisplay.append({"option": "Repair", "clickable": True})}
  
  # Supply option
  if selectedUnits.units_name == "APC" and alliedNeighbors:
    optionsDisplay.append({"option": "Supply"}, "clickable" = True)
  '''
  # Hide options
  if selectedUnit["units_name"] == "Stealth" or selectedUnit["units_name"] == "Sub":
    hideOption = {"option": "", "clickable": True}
    subDive = selectedUnit["units_sub_dive"]
    if subDive == "N" or subDive == "R":
      hideOption["option"] = "Hide"
      optionsDisplay.append(hideOption)
    else: 
      hideOption["option"] = "Unhide"
      optionsDisplay.append(hideOption)

  # Capture and Silo options
  unitTeam = playersInfo[selectedUnit["units_players_id"]]["players_team"]
  if x in buildingsInfo and y in buildingsInfo[x]:
    targetTile = buildingsInfo[x][y]
  else: 
    targetTile = "Terrain"

  if selectedUnit["units_name"] == "Infantry" or selectedUnit["units_name"] == "Mech":
    terrainName = targetTile["terrain_name"] # throws error here when targetTile = "Terrain"

    # following statement is suspect
    if targetTile != "Terrain" and unitTeam != targetTile["buildings_team"] and terrainName != "Silo|Rubble":
      optionsDisplay.append({"option": "Capt", "clickable": True})
    elif terrainName == "Silo":
      optionsDisplay.append({"option": "Launch", "clickable": True})


  # Explode option
  if selectedUnit["units_name"] == "Black Bomb":
    optionsDisplay.append({"options": "Explode", "clickable": True})

  # Fire Option
  # Don't calculate damage for indirects that have moved
  if selectedUnit["units_short_range"] and selectedUnit["units_x"] != x or selected["units_y"] != y:
    pass
  elif selectedUnit["units_ammo"]!= 0 or selectedUnit["units_second_weapon"]:
    unitsInRange = findUnitsInRangeOf(x, y, selectedUnit, clientObjs)
    if (unitsInRange.length != 0):
      unitAmmo = selectedUnit["units_ammo"]
      secondWeapon = selectedUnit["units_second_weapon"]
      fireOption = {"option": "Fire", "clickable": True}

      if not unitAmmo and not secondWeapon:
        fireOption["clickable"] = False
        fireOption["message"] = "Unit has no ammo!"

      optionsDisplay.insert(0, fireOption)
      # I can't tell what current Click is supposed to be, new object?
      #currentClick["unitsInRange"] = unitsInRange

  # Delete option
  if x == selectableUnit["units_x"] and y == selectedUnit["units_y"]:
    optionsDisplay.append({"option": "Delete", "clickable": True})

  # Wait option
  optionsDisplay.append({"option": "Wait", "clickable": True})

  print ("Check Target Tile Ran")
  return optionsDisplay


'''
//Select the available options when clicking on a movement tile
function checkTargetTile(selectedUnit, x, y, clientObjs) {
  const { 
    buildings: buildingsInfo, 
    players: playersInfo, 
    units: unitsInfo, 
    unit_ap: unitMap 
  } = clientObjs;

  const optionsDisplay = [];
  const currentCargo = selectedUnit.units_cargo1_units_id || selectedUnit.units_cargo2_units_id;

  if(unitMap[x] && unitMap[x][y] && selectedUnit.units_id !== unitMap[x][y].units_id) {
    const targetUnitId = unitMap[x][y].units_id;
    const targetUnit = unitsInfo[targetUnitId];
    const targetName = targetUnit.units_name;
    
    //Load option
    const canLoad = checkCargo(targetUnit, selectedUnit);
    const targetCargo = targetUnit.units_cargo1_units_id || targetUnit.units_cargo2_units_id ? true : false;
    if(canLoad) {
      const loadOption = {
        option: "Load",
        clickable: true
      }
      //Transport is full
      if(canLoad !== "Y") {
        loadOption.clickable = false;
        loadOption.message = canLoad;
      }
      optionsDisplay.push(loadOption);
    }
    
    //Join option
    if(targetName === selectedUnit.units_name && targetUnit.units_hit_points < 10 && !targetCargo && !currentCargo) {
      optionsDisplay.push({ option: "Join", clickable: true });
      return optionsDisplay;
    }

    if(optionsDisplay.length !== 0) return optionsDisplay;

    return;
  }
  
  //Unload option
  const isLandingTile = checkLanding(currentCargo, selectedUnit, x, y, clientObjs);
  if(isLandingTile && selectedUnit.units_x === x && selectedUnit.units_y === y) {
    optionsDisplay.push({ option: "Unload", clickable: true });
  } 

  //Repair option
  const neighbours = loopNeighbours(x, y, selectedUnit, clientObjs);
  const alliedNeighbours = neighbours.allied.length !== 0;

  if(selectedUnit.units_name === "Black Boat" && alliedNeighbours) {
    optionsDisplay.push({ option: "Repair", clickable: true });
  }
  //Supply option
  if(selectedUnit.units_name === "APC" && alliedNeighbours) {
    optionsDisplay.push({ option: "Supply", clickable: true });
  }
  //Hide options
  if(selectedUnit.units_name === "Stealth" || selectedUnit.units_name === "Sub") {
    const hideOption = {
      option: "",
      clickable: true
    };
    const subDive = selectedUnit.units_sub_dive;
    if(subDive === "N" || subDive === "R") {
      hideOption.option = "Hide";
      optionsDisplay.push(hideOption);
    } else {
      hideOption.option = "Unhide";
      optionsDisplay.push(hideOption);
    }
  }

  //Capture & Silo options
  const unitTeam = playersInfo[selectedUnit.units_players_id].players_team;
  const targetTile = buildingsInfo[x] && buildingsInfo[x][y] ? buildingsInfo[x][y] : "Terrain";
  if(selectedUnit.units_name === "Infantry" || selectedUnit.units_name === "Mech") {
    const terrainName = targetTile.terrain_name;

    if(targetTile !== "Terrain" && unitTeam !== targetTile.buildings_team && !/Silo|Rubble/.test(terrainName)) {
      optionsDisplay.push({ option: "Capt", clickable: true });
    }
    //Silo
    else if(/(Silo)$/.test(terrainName)) {
      optionsDisplay.push({ option: "Launch", clickable: true });
    }
  }
  //Explode option
  if(selectedUnit.units_name === "Black Bomb") {
    optionsDisplay.push({ option: "Explode", clickable: true });
  }

  //Fire option
  //Don't calculate damage for indirects that have moved
  if(selectedUnit.units_short_range && (selectedUnit.units_x !== x || selectedUnit.units_y !== y)) {

  } else if(selectedUnit.units_ammo !== 0 || selectedUnit.units_second_weapon) {
    //Get units in range of attacker and store in selectedUnit
    const unitsInRange = findUnitsInRangeOf(x, y, selectedUnit, clientObjs);
    if(unitsInRange.length !== 0) {
      const unitAmmo = selectedUnit.units_ammo;
      const secondWeapon = selectedUnit.units_second_weapon;
      const fireOption = {
        option: "Fire",
        clickable: true
      }
      if(!unitAmmo && !secondWeapon) {
        fireOption.clickable = false;
        fireOption.message = "Unit has no ammos!";
      }
      optionsDisplay.unshift(fireOption);
      currentClick.unitsInRange = unitsInRange;
    }
  }
  //Delete option
  if(x === selectedUnit.units_x && y === selectedUnit.units_y) {
    optionsDisplay.push({ option: "Delete", clickable: true });
  } 

  //Wait option
  optionsDisplay.push({ option: "Wait", clickable: true });

  return optionsDisplay;
} '''