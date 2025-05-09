import pandas as pd
from calculation import PREDICATES, find_interesting_games, stream_games,parse_GID
import constants
import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict
import numpy as np
import plotly.io as pio


records = []
merged_file = f'{constants.YEAR}_{constants.SEASON_TYPE}_merged'
file_json = f"{constants.MERGED_DIR}/{merged_file}.json"

def build_team_pair_data(path):
    data = defaultdict(float)      
    details = defaultdict(list)      

    for game_id, triggered in find_interesting_games(path):
        parsed = parse_GID(game_id)
        home_team = parsed['home_team']
        away_team = parsed['away_team']

        total = 0.0
        detail_lines = []
        for pred_name, (weight, metric_val) in triggered.items():
            val = metric_val if isinstance(metric_val, (int, float)) else float(bool(metric_val))
            contrib = weight #* val

            # Add to total
            total += contrib

            # Prepare detail line for this predicate
            detail_lines.append(f"{pred_name}: weight={weight}, value={metric_val}, contrib={contrib:.2f}")

        data[(home_team, away_team)] += total
        details[(home_team, away_team)].extend(detail_lines)

    # Build records including a full detail string joined by <br> for HTML line breaks
    records = []
    for (home, away), value in data.items():
        hover_text = f"Home: {home}<br>Away: {away}<br>Total Value: {value:.2f}<br>" + "<br>".join(details[(home, away)])
        records.append({'home_team': home, 'away_team': away, 'value': value, 'details': hover_text})

    return pd.DataFrame(records)

# Replace this with path to your JSON data file
data_path = file_json

df_pairs = build_team_pair_data(data_path)

# Create mappings from team initials to numbers for axes
home_teams = sorted(df_pairs['home_team'].unique())
away_teams = sorted(df_pairs['away_team'].unique())

home_idx = {team: i for i, team in enumerate(home_teams)}
away_idx = {team: i for i, team in enumerate(away_teams)}

# Coordinates for scatter points
x_vals = [home_idx[ht] for ht in df_pairs['home_team']]
y_vals = [away_idx[at] for at in df_pairs['away_team']]
z_vals = df_pairs['value']
marker_sizes = [8] * len(df_pairs)  
fig = go.Figure()


def cuboid_mesh(x_center, y_center, height, width=0.4, depth=0.4, color='blue'):

    x = np.array([x_center - width/2, x_center + width/2, x_center + width/2, x_center - width/2,
                  x_center - width/2, x_center + width/2, x_center + width/2, x_center - width/2])
    y = np.array([y_center - depth/2, y_center - depth/2, y_center + depth/2, y_center + depth/2,
                  y_center - depth/2, y_center - depth/2, y_center + depth/2, y_center + depth/2])
    z = np.array([0, 0, 0, 0, height, height, height, height])

    I = [0, 0, 0, 1, 2, 4, 5, 6, 7, 1, 2, 3]
    J = [1, 3, 4, 2, 3, 5, 6, 7, 4, 5, 6, 7]
    K = [3, 4, 5, 3, 7, 6, 7, 4, 0, 6, 7, 4]

    return go.Mesh3d(
        x=x,
        y=y,
        z=z,
        color=color,
        opacity=0.8,
        i=I,
        j=J,
        k=K,
        flatshading=True,
        showscale=False
    )

# Generate bars for each data point
for x, y, height, val in zip(x_vals, y_vals, df_pairs['value'], df_pairs['value']):

    bar = cuboid_mesh(x, y, height, width=0.6, depth=0.6, color='blue') 
    fig.add_trace(bar)

fig.add_trace(go.Scatter3d(
    x=x_vals,
    y=y_vals,
    z=df_pairs['value'],
    mode='markers',
    marker=dict(
        size=4,
        color=df_pairs['value'],
        colorscale='Viridis',
        colorbar=dict(title='Weighted Metric'),
        opacity=1,
    ),
    text=df_pairs['details'],
    hoverinfo='text'
))

fig.update_layout(
    title='3D Bar Chart of Predicate Metric by Team Matchups',
    scene=dict(
        xaxis=dict(
            title='Home Team',
            tickvals=list(home_idx.values()),
            ticktext=list(home_idx.keys()),
        ),
        yaxis=dict(
            title='Away Team',
            tickvals=list(away_idx.values()),
            ticktext=list(away_idx.keys()),
        ),
        zaxis=dict(title='Metric Value'),
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    height=700,
    width=900
)
pio.write_html(fig, file=f"graphs/{merged_file}_AllTeamsCompared_3D.html", full_html=True)

