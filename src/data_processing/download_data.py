import season_game_results
import preprocessing
import get_games
import json
import merge_json
from constants import YEAR,SEASON,SEASON_TYPE,SEASONS_DIR,SEASON_DIR,REFINED_DIR,MERGED_DIR

verbosity = True

allgame_path = season_game_results.get_allgames(SEASON,
                                                base_path=SEASONS_DIR,
                                                seasontype=SEASON_TYPE,
                                                verbose=verbosity,
                                                replace=True)


with open(allgame_path, "r") as f:
    allgames = json.load(f)


num_games = len(allgames)
for i in range(0,num_games):
    fullgame = preprocessing.fullgame_merge(allgames[i],input_dir=SEASON_DIR)
    preprocessing.save_refined_gamelog(allgames[i],fullgame,base_path=REFINED_DIR,replace=False,verbose=verbosity)

out = f'{MERGED_DIR}/{YEAR}_{SEASON_TYPE}_merged.json'
merge_json.merge_jsons(REFINED_DIR, out)

                     