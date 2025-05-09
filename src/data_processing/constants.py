YEAR = 2025
SEASON = f"{YEAR - 1}-{YEAR % 100:02}" 

SEASON_TYPE = "Playoffs" # "Playoffs" or "Regular Season"
MERGED_DIR = "SavedData/FullMergedData"
SEASONS_DIR = f"SavedData/{SEASON_TYPE}/SeasonData"
SEASON_DIR = f"SavedData/{SEASON_TYPE}/{YEAR}/GameData"
REFINED_DIR =f"SavedData/{SEASON_TYPE}/{YEAR}/RefinedGamelogs"

