import pandas as pd
import plotly.express as px
from calculation import PREDICATES, find_interesting_games, stream_games,parse_GID
import constants
import plotly.io as pio 
import pandas as pd
import plotly.graph_objects as go

records = []
merged_file = f'{constants.YEAR}_{constants.SEASON_TYPE}_merged'
file_json = f"{constants.MERGED_DIR}/{merged_file}.json"


def build_bars(path):
    rows = []
    for game_id, triggered in find_interesting_games(path):
        parsed = parse_GID(game_id)
        home_team = parsed['home_team']
        away_team = parsed['away_team']

        for pred_name, (weight, value) in triggered.items():
            height = value if isinstance(value, (int, float)) else int(bool(value))

            rows.append({
                'game_id': game_id,
                'team': home_team,
                'predicate': pred_name,
                'weight': weight,
                'height': height,
            })
            rows.append({
                'game_id': game_id,
                'team': away_team,
                'predicate': pred_name,
                'weight': weight,
                'height': height,
            })

    return pd.DataFrame(rows)

df_bars = build_bars(file_json)


fig = go.Figure()

teams = sorted(df_bars['team'].unique())
predicates = df_bars['predicate'].unique()

fig = go.Figure()

for pred in predicates:
    pred_df = df_bars[df_bars['predicate'] == pred]

    y_values = []
    for team in teams:
        team_df = pred_df[pred_df['team'] == team]
        if team_df.empty:
            y_values.append(0)
        else:
            y_values.append(team_df['weight'].sum())

    fig.add_trace(go.Bar(
        name=pred,
        x=teams,
        y=y_values,
        text=[f'{v:.2f}' for v in y_values],
        textposition='auto',
    ))

fig.update_layout(
    barmode='group',
    title='Predicate Weights for Each Team',
    xaxis_title='Team',
    yaxis_title='Total Weight',
)

pio.write_html(fig, file=f"graphs/{merged_file}_SingleGamAppeal_ByWeight.html", full_html=True)


