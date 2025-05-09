import requests
import pandas as pd
from pathlib import Path
import json
import utils as utils

def get_allgames(
    season,
    seasontype="Regular Season",
    base_path="SavedData/GameData",
    replace=False,
    verbose=False
):
    """
    Fetch all games for a given season/seasontype unless
    the file already exists and replace==False.
    Returns the path to the JSON file on disk.
    """

    get_games_url = "https://api.pbpstats.com/get-games/nba"

    folder   = Path(base_path)
    fname    = f"{season}_{seasontype.replace(' ', '')}_AllGames.json"
    fullpath = folder / fname

    if not utils.verify_file(fullpath, replace=replace, verbose=verbose):
        return str(fullpath)


    params = {"Season": season, "SeasonType": seasontype}
    resp   = requests.get(get_games_url,
                          params=params,
                          headers={"accept": "application/json"})
    resp.raise_for_status()
    games  = resp.json().get("results", [])

    # Write the JSON to fullpath
    with open(fullpath, "w") as f:
        json.dump(games, f, indent=4)

    if verbose:
        print(f"Fetched {season}'s {len(games)} game data to {fullpath}")

    return str(fullpath)
