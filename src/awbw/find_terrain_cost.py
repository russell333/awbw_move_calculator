# findTerrainCost


def findTerrainCost(mType, x, y, unitTeam, player, clientObjs):
  #movecosts = clientObjs.moveCosts



  print ("findTerrainCost activated")
  return
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