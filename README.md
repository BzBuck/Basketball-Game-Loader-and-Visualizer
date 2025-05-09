# NBA Game Appeal Visualizer

## Overview  
The NBA Game Appeal Visualizer is a data-driven project that evaluates and visualizes the "interest level" of NBA games based on various key factors. Using a large dataset of detailed game statistics combined with innovative calculations, this tool helps basketball fans and enthusiasts discover the most engaging games to watch. The project processes raw game data into insightful visualizations, making it accessible both for data-savvy users and casual fans looking for exciting matchups.

The tool is designed for basketball fans, statistics enthusiasts, and anyone interested in discovering the most exciting NBA games. Its flexible interface ensures accessibility for casual users as well as those who want deeper analytic insights.

---
# Usage

To download all of data needed to run everything

`python src/data_processing/download_data.py`

This downloads all of the files needed. It takes a very long time to generate because of rate limits.

To create the visualizations run the files in the visualization folder

`python src/visualization/3D_team_comparison.py`
`python src/visualization/interest_ratings.py`
`python src/visualization/interest_weighted.py`

These files will be generated in the graphs folder.
---
# Project Directory Structure


```
.
├── README.md
├── graphs
│   ├── 2025_Playoffs_merged_AllTeamsCompared_3D.html
│   ├── 2025_Playoffs_merged_SingleGamAppeal_ByWeight.html
│   ├── 2025_Playoffs_merged_SingleGameAppeal.html
│   ├── 2025_Regular Season_merged_AllTeamsCompared_3D.html
│   ├── 2025_Regular Season_merged_SingleGamAppeal_ByWeight.html
│   └── 2025_Regular Season_merged_SingleGameAppeal.html
├── requirements.txt
└── src
    ├── data_processing
    │   ├── __pycache__
    │   │   ├── constants.cpython-311.pyc
    │   │   ├── get_games.cpython-311.pyc
    │   │   ├── merge_json.cpython-311.pyc
    │   │   ├── preprocessing.cpython-311.pyc
    │   │   ├── season_game_results.cpython-311.pyc
    │   │   └── utils.cpython-311.pyc
    │   ├── constants.py
    │   ├── download_data.py
    │   ├── get_games.py
    │   ├── merge_json.py
    │   ├── preprocessing.py
    │   ├── season_game_results.py
    │   └── utils.py
    └── visualization
        ├── 3D_team_comparison.py
        ├── __pycache__
        │   ├── calculation.cpython-311.pyc
        │   └── constants.cpython-311.pyc
        ├── calculation.py
        ├── constants.py
        ├── interest_ratings.py
        └── interest_weighted.py

```
9 directories, 30 files

---

## Project Scope  
This project quantifies how interesting each NBA game is by analyzing multiple parameters, including:  
- How close and competitive the game was  
- Significant comebacks during the game  
- Outstanding individual player performances  
- Outlier numbers

To ensure the quality and accuracy of this evaluation formula, the calculated appeal scores are compared against real-world engagement indicators, like the number of views on game highlight videos.

---

## Data Collection & Processing  
- Data is collected directly from the **PBPstats API**, encompassing detailed play-by-play stats and player information for every game.  
- Raw data is processed by merging three base JSON datasets per game into a unified, consolidated format.  
- The complete dataset for all games is approximately **28 million lines of JSON** data / 1GB for the regular season merged file  
- To optimize performance and relevancy, a filtering system extracts only the attributes relevant to game appeal, reducing data complexity and size by removing extraneous player-quarter level details.  
- Both merged single-file and multi-file approaches are supported, allowing flexible experimentation with data handling strategies.

---

## Visualization Features  
The visualizer presents NBA game appeal through several interactive and customizable views. They use plotly graphs and are stored in the visualization folder as html  

- **Team-Based Bar Graphs**  
  Display each team’s game appeal values over time, with game number on the x-axis and appeal score on the y-axis.

- **3D Comparative Graph**  
  Visualize appeal across multiple teams simultaneously, using a z-axis for teams. (Note: 3D visualizations come with inherent complexity but provide a unique comparative perspective.)

- **Player-Centric Analysis**  
  Identify players who most frequently appear in high-appeal games.

- **Dynamic Filtering System**  
  Users can input specific parameters—teams, games, players—via command-line arguments or interactive menus to tailor the visualizations to their interests.

---


## Future Improvements  
- Further refinement and tuning of the appeal evaluation formula to capture the nuances of game excitement more accurately.  
- Enhanced visualizations with richer interactivity and real-time data updates.  
- Integration of additional engagement metrics for validation and improved scoring accuracy.
- Add easy stat search features using available keys shared

---

## Acknowledgments  
This project utilizes data made accessible via the **PBPstats API** and leverages large-scale data processing techniques to deliver innovative sports visualizations.

# Basketball-Game-Loader-and-Visualizer
