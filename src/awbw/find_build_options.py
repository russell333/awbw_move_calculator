def findBuildOptions(x, y, clientObjs):
	banUnits = clientObjs.banunits
	buildingsInfo = clientObjs.buildings
	genericUnits = clientObjs.generic_units
	labUnits = clientObjs.labunits
	playersInfo = clientObjs.players 
	viewerPId = clientObjs.viewerPId

	if x not in buildingsInfo or y not in buildingsInfo[x]:
		buildOptions = []
		return buildOptions
	building = buildingsInfo[x][y]
	buildingName = building["terrain_name"]
	coName = playersInfo[viewerPId]["co_name"]
	coPower = playersInfo[viewerPId]["players_co_power_on"]
	playerFunds = playersInfo[viewerPId]["players_funds"]

	mTypes = []

	# Get what units can be built
	if "Base" in buildingName or ("City" in buildingName and coName == "Hachi" \
		and coPower == "S"):
		mTypes = ["F", "B", "T", "W", "P"]
	elif "Airport" in buildingName:
		mTypes = ["A"]
	elif "Port" in buildingName:
		mTypes = ["L", "S"]
	if not mTypes: return

	buildOptions = []

	hasLabs = playersInfo[viewerPId]["labs"] if playersInfo[viewerPId]["labs"] else 0

	# check for CO-specific fund multipliers
	costMultiplier = 1
	if coName == "Colin": costMultiplier = 0.8
	if coName == "Hachi": costMultiplier = 0.9
	if coName == "Hachi" and coPower == "C" or coPower == "S": costMultiplier = 0.5
	if coName == "Kanbei": costMultiplier = 1.2

	for unitName in genericUnits.keys:
		# Skip banned units
		if banUnits and banUnits[unitName]: continue

		# Skip lab units when you have no lab
		if labUnits and labUnits[unitName] and not hasLabs: continue

		mType = genericUnits[unitName]["units_movement_type"]
		unitCost = genericUnits[unitName]["units_cost"]

		if mType in mTypes and unitCost*costMultiplier <= playerFunds:
			buildOptions.append(genericUnits[unitName]["units_name"])
	#print (buildOptions)
	buildOptions.sort()
	return buildOptions


'''
//Find the units a player can buy upon clicking a property
//genericUnits, banUnits and labUnits are global objects

function findBuildOptions(x, y, clientObjs) {
  const { 
    banunits: banUnits, 
    buildings: buildingsInfo, 
    generic_units: genericUnits, 
    labunits: labUnits, 
    players: playersInfo, 
    viewerPId 
  } = clientObjs;

  const building = buildingsInfo[x][y];
  const buildingName = building.terrain_name;
  const coName = playersInfo[viewerPId].co_name;
  const coPower = playersInfo[viewerPId].players_co_power_on;
  const playerFunds = playersInfo[viewerPId].players_funds;
  
  let mTypes;

  //Get what units can be built
  if(/Base/.test(buildingName) || (/City/.test(buildingName) && coName === "Hachi" && coPower === "S")) {
    mTypes = ["F", "B", "T", "W", "P"];
  } 
  else if(/Airport/.test(buildingName)) {
    mTypes = ["A"];
  } 
  else if(/Port/.test(buildingName)) {
    mTypes = ["L", "S"];
  }
  if(!mTypes) return;

  const buildOptions = [];

  const hasLabs = playersInfo[viewerPId].labs !== 0;
  
  for(const unitName in genericUnits) {
    //Skip banned units
    if(banUnits && banUnits[unitName]) continue;

    //Skip lab units
    if(labUnits && labUnits[unitName] && !hasLabs) continue;

    const mType = genericUnits[unitName].units_movement_type;
    const unitCost = genericUnit[unitName].units_cost;
    
    if(mTypes.includes(mType) && unitCost >= playerFunds) {
      buildOptions.push(genericUnits[unitName]);
    }
  }
  const sortedOptions = buildOptions.sort(function(a, b) {
    return a.units_cost - b.units_cost;
  });

  return sortedOptions;
}
'''