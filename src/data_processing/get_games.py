import requests
import pandas as pd
import json
import time
from collections import defaultdict
import utils as utils
from pathlib import Path



def save_game(
    game,
    base_path='SavedData/Gamelogs/',
    delay=5,
    replace=False,
    players="Player",
    verbose=False
):
    """Saves game logs from the PBPStats API to a JSON file."""
    # Copy + set type
    params = game.copy()
    params['Type'] = players

    # Build filename & full path
    filename = (
        f"{game['GameId']}_"
        f"{game['Date'].replace('-', '')}_"
        f"{game['HomeTeamAbbreviation']}_{game['HomePoints']}_"
        f"{game['AwayTeamAbbreviation']}_{game['AwayPoints']}_"
        f"{params['Type']}.json"
    )
    gl_path = Path(base_path) / filename

    # Use your existing verify_file in one shot
    if not utils.verify_file(gl_path, replace=replace, verbose=verbose):
        return str(gl_path)

    # Rate‐limit guard
    time.sleep(delay / 2)
    try:
        resp = requests.get(
            "https://api.pbpstats.com/get-game-stats",
            params=params,
            headers={"accept": "application/json"}
        )
        resp.raise_for_status()
        data = resp.json()

        # Write it out
        with open(gl_path, "w") as fp:
            json.dump(data, fp, indent=4)

        if verbose:
            print("Game log saved:", gl_path)
        return str(gl_path)

    except requests.exceptions.RequestException as e:
        print("API request failed:", e)
        return None

    finally:
        time.sleep(delay / 2)

