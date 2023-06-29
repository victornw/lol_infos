# Input de região e nick
# output: Lvl, elo ranked, 5 ultimas rankeds 
import requests

print("This application needs a PRIVATE RIOT API to work, get yours at https://developer.riotgames.com/")
def getId(summoner, region, api_key):
  try:
    api_url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner + "?api_key=" + api_key
    resp = requests.get(api_url)
    infos = resp.json()
    return infos["summonerLevel"], infos["id"], infos["puuid"]
  except:
    print("ERROR")
    quit()

def getElo(id, region,api_key):
  api_url = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + id + "?api_key=" + api_key
  resp = requests.get(api_url).json()
  return resp[0]["tier"] + " " + resp[0]["rank"]

def getMatch(puuid, api_key,region):
  api_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?type=ranked&start=0&count=20" + "&api_key=" + api_key
  matches = (requests.get(api_url).json())[:5]
  winstreak = ""
  for i in range(5):
    api_url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + matches[i] + "?api_key=" + api_key
    resp = requests.get(api_url).json()
    player = resp["metadata"]["participants"].index(puuid)
    teamOneCheck = resp["info"]["teams"][0]["win"]
    if player < 5 and teamOneCheck == True: 
      winstreak += "W"
    elif player >= 5 and teamOneCheck == False:
      winstreak += "W"
    else: winstreak += "L"

  return winstreak


summ = input("Summoner: ")
name = summ.replace(" ","").lower()
region = input("Region (BR1/NA1): ")
api_key = input("API KEY: ")

getid = getId(name,region,api_key)
level = getid[0]
id = getid[1]
puuid = getid[2]

history = (getMatch(puuid,api_key, region))
elo = (getElo(id, region, api_key))
print("=" * 20)
print(f"Summoner: {summ} \nLevel: {level} \nElo: {elo} \nLast 5: {history}")
