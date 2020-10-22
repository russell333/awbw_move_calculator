# Used in getMovementTiles

def findTerrainCost(maxX, maxY, mType, x, y, unitTeam, player, clientObjs):
  moveCosts = clientObjs.movecosts
  unitMap = clientObjs.unit_map

  coName = player["co_name"]
  power = player["players_co_power_on"]
  weatherCode = clientObjs.game.games_weather_code

  if x > (maxX-1) or x < 0 or y < 0 or y > (maxY-1):
    return 10000 # supposed to be "null"
    
  if x in unitMap and y in unitMap[x] and str(unitMap[x][y]["team"]) != str(unitTeam):
    #print (unitMap[x][y]["team"])
    return "A"

  
  # Special cases for Olaf and Drake
  if coName == "Olaf" and weatherCode == "S": weatherCode = "C"
  if coName == "Drake" and weatherCode == "R": weatherCode = "C"

  # "moveCosts is global"
  mCost = moveCosts[x][y][weatherCode][mType]

  # special cases for Sturm/Lash
  if mCost and weatherCode != "S":
    if coName == "Sturm" or (coName == "Lash" and power != "N"):
      mCost = 1
  
  return mCost
'''
//Used in getMovementTiles
function findTerrainCost(mType, x, y, unitTeam, player, clientObjs) {
  const {
     movecosts: moveCosts, 
     unit_map: unitMap, 
  } = clientObjs;


  const coName = player.co_name;
  const power = player.players_co_power_on;
  const weatherCode = clientObjs.game.games_weather_code;

  if (x > (maxX - 1) || x < 0 || y < 0 || y > (maxY - 1)) {
    return null;
  }

  //Mark tile as A for tiles where there is an attackable unit
  if(unitMap[x] && unitMap[x][y] && unitMap[x][y].team != unitTeam) {
    return "A";
  }

  //Special cases for Olaf and Drake
  if (coName === "Olaf" && weatherCode === "S") { weatherCode = "C"; }
  if (coName === "Drake" && weatherCode === "R") { weatherCode = "C"; }

  //moveCosts is global
  let mCost = moveCosts[x][y][weatherCode][mType];

  //Special cases for Sturm/Lash
  if(mCost && weatherCode !== "S") {
    if(coName === "Sturm" || (coName === "Lash" && power !== "N")) {
      mCost = 1; 
    }
  }
  return mCost;
} '''