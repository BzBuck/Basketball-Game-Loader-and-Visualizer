import plotly.graph_objects as go
import plotly.io as pio 
from collections import defaultdict
from calculation import PREDICATES, find_interesting_games
import constants

all_reasons = set(PREDICATES.keys())
reason_weights = defaultdict(list)
reason_details = defaultdict(list)
game_ids = []
merged_file = f'{constants.YEAR}_{constants.SEASON_TYPE}_merged'
file_json = f"{constants.MERGED_DIR}/{merged_file}.json"

for gid, reasons in find_interesting_games(file_json):
    game_ids.append(gid)
    for reason in all_reasons:
        if reason in reasons:
            weight = reasons[reason][0]
            details = reasons[reason][1]
            reason_weights[reason].append(weight)
            # Create human-readable summary string for details:

            if isinstance(details, list):
                # List of (player, value) tuples
                detail_str = ', '.join(f"{player}: {value}" for player, value in details)
            else:
                # Just a number or string detail
                detail_str = str(details)

            reason_details[reason].append(detail_str)
        else:
            reason_weights[reason].append(0)
            reason_details[reason].append('')  # no detail
# Total weights (for sorting)
total_weights = {gid: sum(reason_weights[r][i] for r in all_reasons) for i, gid in enumerate(game_ids)}

# Sort game IDs based on total weight (descending order)
sorted_games = sorted(total_weights.keys(), key=lambda gid: total_weights[gid], reverse=True)

# Rearrange reason weights and details based on sorted order
sorted_reason_weights = {reason: [reason_weights[reason][game_ids.index(gid)] for gid in sorted_games] for reason in all_reasons}
sorted_reason_details = {reason: [reason_details[reason][game_ids.index(gid)] for gid in sorted_games] for reason in all_reasons}

# Update traces with sorted game order
traces = []
for reason in sorted(all_reasons):
    traces.append(go.Bar(
        x=sorted_games,
        y=sorted_reason_weights[reason],
        name=reason,
        customdata=[f"Details: {detail}" for detail in sorted_reason_details[reason]],
        hovertemplate=(
            'Game: %{x}<br>' +
            'Reason: %{fullData.name}<br>' +
            'Weight: %{y}<br>' +
            '%{customdata}<extra></extra>'
        ),
    ))

fig = go.Figure(data=traces)

fig.update_layout(
    barmode='stack',
    title='Interesting Game Scores by Reason',
    xaxis_title='Game ID',
    yaxis_title='Weight Contribution',
    xaxis_tickangle=45,
    template='plotly_white',
    height=600,
    width=1000,
)

pio.write_html(fig, file=f"graphs/{merged_file}_SingleGameAppeal.html", full_html=True)
