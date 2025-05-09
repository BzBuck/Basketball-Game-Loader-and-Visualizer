
import ijson


def stream_games(path):
    """
    Yields (game_id, game_data) for each top‐level entry in the JSON.
    """
    with open(path, 'rb') as f:
        for game_id, game_data in ijson.kvitems(f, ''):
            yield game_id, game_data

def parse_GID(game_id):
    """Extract game details from a game ID string."""
    keys = ["game_id", "date", "home_team", "home_pts", "away_team", "away_pts"]
    return dict(zip(keys, game_id.split('_')))


def is_close_game(game_id, max_diff=5):
    game_info = parse_GID(game_id)  
    home = int(game_info["home_pts"])  
    away = int(game_info["away_pts"])
    
    return abs(home - away) <= max_diff


def had_large_comeback(game_data, down_by=10):
    # Track halftime and full-game scores
    half = {'Away': 0, 'Home': 0}
    full = {'Away': 0, 'Home': 0}

    for side in ('Away', 'Home'):
        for period, players in game_data.get('stats', {}).get(side, {}).items():
            for p in players:
                pts = int(p.get('Pts', p.get('Points', 0)))
                full[side] += pts
                if period in ('1', '2'):  # First half
                    half[side] += pts

    # Calculate score differences
    half_diff = half['Home'] - half['Away']
    full_diff = full['Home'] - full['Away']

    # Determine if a comeback happened and return the comeback size
    if half_diff >= down_by and full_diff < 0:  # Home team comeback
        comeback_size = abs(half_diff - full_diff)
        return comeback_size
    elif half_diff <= -down_by and full_diff > 0:  # Away team comeback
        comeback_size = abs(half_diff - full_diff)
        return comeback_size

    return 0  # No significant comeback


def any_outlier_performance(game_data, metric, thresh=1, sign="eq", include_periods=["FullGame"]):
    totals = {}

    for side in ('Away', 'Home'):
        periods = game_data.get('stats', {}).get(side, {})

        for period, players in periods.items():
            if period not in include_periods and period != include_periods:
                continue

            for p in players:
                stat = int(p.get(metric, 0))
                name = p.get('Name')
                totals[name] = totals.get(name, 0) + stat

    # Apply the correct comparison based on sign
    matched_players = [
        (name, stat) for name, stat in totals.items() if (
            (sign == "eq" and stat == thresh) or
            (sign == "gt" and stat > thresh) or
            (sign == "lt" and stat < thresh) or
            (sign == "ge" and stat >= thresh) or
            (sign == "le" and stat <= thresh)
        )
    ]

    return matched_players  




# description, weight, measure function
PREDICATES = {
    'scoring_performance':    (4, lambda gid, data: any_outlier_performance(data,"Points", thresh=45, sign="ge", include_periods="FullGame")),
    '4th_qscoring_performance':    (2, lambda gid, data: any_outlier_performance(data,"Points", thresh=15, sign="ge", include_periods="4")),
    'rebounding_performance': (1, lambda gid, data: any_outlier_performance(data,"Rebounds", thresh=20, sign="ge", include_periods="FullGame")),
    'assisting_performance': (1, lambda gid, data: any_outlier_performance(data,"Assists", thresh=15, sign="ge", include_periods="FullGame")),
    'close_game':             (5, lambda gid, data: is_close_game(gid, max_diff=5)),
    'big_comeback':           (5, lambda gid, data: had_large_comeback(data, 10)),  
}

def find_interesting_games(path):
    for game_id, game_data in stream_games(path):
        triggered = {}
        for name, (weight, pred) in PREDICATES.items():
            try:
                result = pred(game_id, game_data)
                if result:
                    triggered[name] = [weight,result]
            except Exception as e:
                continue

        if triggered:
            yield game_id, triggered

