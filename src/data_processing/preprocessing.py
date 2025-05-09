import utils as utils
import season_game_results
import get_games
import json
from pathlib import Path
from collections import defaultdict


def merge_values(val1, val2):
    # If both values can be converted to float then add them
    try:
        num1 = float(val1)
        num2 = float(val2)
        # when both values are whole numbers you might want to convert back to int:
        summed = num1 + num2
        if summed.is_integer():
            return int(summed)
        else:
            return summed
    except (TypeError, ValueError):
        # Otherwise, join as strings (ignoring any that are None)
        parts = []
        if val1 is not None:
            parts.append(str(val1))
        if val2 is not None:
            parts.append(str(val2))
        return "-".join(parts)
    
# Function to merge a list of dictionaries using merge_values
def merge_lineup_dicts(dict_list):
    merged_dict = {}
    for d in dict_list:
        for key, value in d.items():
            if key in merged_dict:
                merged_dict[key] = merge_values(merged_dict[key], value)
            else:
                merged_dict[key] = value
    return merged_dict


def form_lu_stats(pl_stats, lu_stats, opponent=False):

    # For each entity id found in a lineup record, track that lineup record.
    lineup_lookup = defaultdict(list)
    for lineup in lu_stats:
        # Avoid rebuilding the list repeatedly by splitting once:
        entity_ids = lineup["EntityId"].split('-')
        for eid in entity_ids:
            lineup_lookup[eid].append(lineup)

    # Instead of building a separate all_stats list, attach diff_stats to each player record.
    for player in pl_stats:
        # Quickly find all related lineup records for this player's entityid
        matching_lineups = lineup_lookup.get(player["EntityId"], [])
   
        # Merge all lineup dictionaries for the player into a new dictionary
        merged_lineup_stats = merge_lineup_dicts(matching_lineups)
        
        if opponent:
            player["opponent_stats"] = merged_lineup_stats
     
        else:
            diff_stats = {}
            player1 = merged_lineup_stats
            player2 = player

            for key, value in player1.items():
                # If the value is numeric, compute the difference.
                if isinstance(value, int):
                    other_value = player2.get(key, 0)
                    if not isinstance(other_value, int):
                        other_value = 0
                    diff_stats[key] = value - other_value
                else:
                    # If this key is one you want to keep (for example, "PlayerName"), copy it.
          
                    if key in ("PlayerName", "SomeOtherNameField"):
                        diff_stats[key] = value

            # Attach the computed diff_stats as a subfield of the player dictionary.  
            player["lineup_diff_stats"] = diff_stats

    return pl_stats  # return the updated player stats list


def fullgame_merge(game,input_dir='SavedData/Gamelogs/'):
    # Check that the files exist and save them
    pl_path = get_games.save_game(game,base_path=input_dir, players="Player")
    lu_path = get_games.save_game(game,base_path=input_dir, players="Lineup")
    op_path = get_games.save_game(game,base_path=input_dir, players="LineupOpponent")

    # Load JSON file
    with open(pl_path, "r") as file:
        pl_game = json.load(file)

    with open(lu_path, "r") as file:
        lu_game = json.load(file)

    with open(op_path, "r") as file:
        op_game = json.load(file)

    adjusted_stats = {}
    # Extract all stats categorized by location and quarter
    for location in pl_game["stats"].keys():
        # Create 'stats' key if not exists.
        adjusted_stats.setdefault("stats", {})
        # Create location key if not exists.
        adjusted_stats["stats"].setdefault(location, {})
        for quarter in pl_game["stats"][location].keys():
            # Access nested structure
            pl_stats = pl_game["stats"][location][f"{quarter}"]
            lu_stats = lu_game["stats"][location][f"{quarter}"]
            op_stats = op_game["stats"][location][f"{quarter}"]

            player_lineup = form_lu_stats(pl_stats, lu_stats)
            player_lineup_op = form_lu_stats(player_lineup, op_stats,opponent=True)
            adjusted_stats["stats"][location][f"{quarter}"] = player_lineup_op

    return adjusted_stats

def save_refined_gamelog(
    game,
    json_data,
    base_path='SavedData/RefinedGamelogs/',
    replace=False,
    verbose=False
) -> bool:
    # 1) Build the output filename & full path
    filename = (
        f"{game['GameId']}_"
        f"{game['Date'].replace('-', '')}_"
        f"{game['HomeTeamAbbreviation']}_"
        f"{game['HomePoints']}_"
        f"{game['AwayTeamAbbreviation']}_"
        f"{game['AwayPoints']}.json"
    )
    full_path = Path(base_path) / filename

    # 2) Let verify_file mkdir the parent, check exists/replace, etc.
    if not utils.verify_file(full_path, replace=replace, verbose=verbose):
        # file exists and replace==False → bail out
        return False

    # 3) Safe to write/overwrite
    with open(full_path, 'w') as fp:
        json.dump(json_data, fp, indent=4)
    if verbose:
        print(f"Wrote {full_path}")
    return True
