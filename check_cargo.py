
def checkCargo(transportUnit, cargoUnit):
  firstCargo = transportUnit["units_cargo1_units_id"]
  secondCargo = transportUnit["units_cargo2_units_id"]
  mType = cargoUnit["units_movement_type"]
  fullMsg = "Transport is full"
  if cargoUnit["units_name"] == "Infantry" or cargoUnit["units_name"] == "Mech":
    if transportUnit["units_name"] == "APC" or transportUnit["units_name"] == "T-Copter":
      if not firstCargo:
        return "Y"
      return fullMsg

    elif (transportUnit["units_name"] == "Black Boat"):
      if not firstCargo or not secondCargo:
        return "Y"
      return fullMsg
  if (cargoUnit["units_name"] == "B-Copter" or cargoUnit["units_name"] == "T-Copter") \
  and transportUnit["units_name"] == "Cruiser":
    if not firstCargo or not secondCargo:
      return "Y"
    return fullMsg
  elif (mType == "A" and transportUnit["units_name"] == "Carrier"):
    if not firstCargo or not secondCargo:
      return "Y"
    return fullMsg
  elif mType != "A" and mType != "L" and mType != "S" \
  and transportUnit["units_name"] == "Lander":
    if not firstCargo or not secondCargo:
      return "Y"
    return fullMsg
  return False

'''//Check if unit is able to load in transport
function checkCargo(transportUnit, cargoUnit) {
  const firstCargo = transportUnit.units_cargo1_units_id;
  const secondCargo = transportUnit.units_cargo2_units_id;
  const mType = cargoUnit.units_movement_type;
  const fullMsg = "Transport is full!";

  if(cargoUnit.units_name === "Infantry" || cargoUnit.units_name === "Mech") {
    if(transportUnit.units_name === "APC" || transportUnit.units_name === "T-Copter") {

      if(!firstCargo) {
        return "Y";
      }
      return fullMsg;
  
    } 
    else if(transportUnit.units_name === "Black Boat") {

      if(!firstCargo || !secondCargo) {
        return "Y";
      }
      return fullMsg;
    }
  } 
  if((cargoUnit.units_name === "B-Copter" || cargoUnit.units_name === "T-Copter") && transportUnit.units_name === "Cruiser") {
    if(!firstCargo || !secondCargo) {
      return "Y";
    } else {
      return fullMsg
    }
  } 
  else if(mType === "A" && transportUnit.units_name === "Carrier") {
    if(!firstCargo || !secondCargo) {
      return "Y";
    }
    return fullMsg; 

  } 
  else if(mType !== "A" && mType !== "L" && mType !== "S" && transportUnit.units_name === "Lander") {
    if(!firstCargo || !secondCargo) {
      return "Y";
    }
    return fullMsg;
  }
  return false;
}'''