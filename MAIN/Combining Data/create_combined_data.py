import pandas as pd

# Importing all the files data
games = pd.read_csv("Data/games.csv")
players = pd.read_csv("Data/players.csv")
plays = pd.read_csv("Data/plays.csv")

week1 = pd.read_csv("Data/tracking_week_1.csv")
week2 = pd.read_csv("Data/tracking_week_2.csv")
week3 = pd.read_csv("Data/tracking_week_3.csv")
week4 = pd.read_csv("Data/tracking_week_4.csv")
week5 = pd.read_csv("Data/tracking_week_5.csv")
week6 = pd.read_csv("Data/tracking_week_6.csv")
week7 = pd.read_csv("Data/tracking_week_7.csv")
week8 = pd.read_csv("Data/tracking_week_8.csv")
week9 = pd.read_csv("Data/tracking_week_9.csv")

tracking_all_weeks = pd.concat(
    [week1, week2, week3, week4, week5, week6, week7, week8, week9], ignore_index=True
)

# Selecting specific features
players_selected = players[["nflId", "displayName", "position"]]
games_selected = games[["gameId", "homeTeamAbbr", "visitorTeamAbbr"]]
plays_selected = plays[
    [
        "gameId",
        "playId",
        "possessionTeam",
        "passResult",
        "passLength",
        "isDropback",
        "rushLocationType",
        "homeTeamWinProbabilityAdded",
        "visitorTeamWinProbilityAdded",
        "expectedPointsAdded",
        "pff_runConceptPrimary",
        "pff_runConceptSecondary",
        "pff_runPassOption",
        "pff_passCoverage",
        "pff_manZone",
        "absoluteYardlineNumber",
        "quarter",
        "down",
        "yardsToGo",
        "playDescription",
    ]
]

# Merging game and play data
merged_data = pd.merge(games_selected, plays_selected, on="gameId")
merged_data_sorted = merged_data.sort_values(by=["gameId", "playId"])

# Merging tracking data with possession team
tracking_with_possession = pd.merge(
    tracking_all_weeks,
    merged_data_sorted[["gameId", "playId", "possessionTeam"]],
    on=["gameId", "playId"],
)

# Filter rows where the possession team matches the club and frameType is BEFORE_SNAP
tracking_possession_team = tracking_with_possession[
    (tracking_with_possession["club"] == tracking_with_possession["possessionTeam"])
    & (tracking_with_possession["frameType"] == "BEFORE_SNAP")
]

# Add player position information to tracking data
tracking_with_position = pd.merge(
    tracking_possession_team,
    players_selected,
    on="nflId",
    how="left",
)

# Calculate total distance traveled by possession team during a play
total_distance_possession_team = (
    tracking_possession_team.groupby(["gameId", "playId"])["dis"]
    .sum()
    .reset_index()
    .rename(columns={"dis": "totalDistanceTraveledByPossessionTeam"})
)

# Calculate distances traveled for each position during a play
distance_by_position = (
    tracking_with_position.groupby(["gameId", "playId", "position"])["dis"]
    .sum()
    .reset_index()
)

# Pivot the data to get distances for each position as columns
distance_by_position_pivot = distance_by_position.pivot(
    index=["gameId", "playId"], columns="position", values="dis"
).fillna(0)

# Rename columns for clarity
distance_by_position_pivot.columns = [
    f"distance_{pos}" for pos in distance_by_position_pivot.columns
]
distance_by_position_pivot = distance_by_position_pivot.reset_index()

# Merge position distances and total possession distance into the main data
combined_data_with_distance = pd.merge(
    merged_data_sorted, distance_by_position_pivot, on=["gameId", "playId"], how="left"
)
combined_data_with_distance = pd.merge(
    combined_data_with_distance,
    total_distance_possession_team,
    on=["gameId", "playId"],
    how="left",
)

# Reordering data for better visibility
columns_order = (
    ["gameId", "playId", "totalDistanceTraveledByPossessionTeam"]
    + [
        col
        for col in combined_data_with_distance.columns
        if col.startswith("distance_")
    ]
    + [
        col
        for col in merged_data_sorted.columns
        if col not in ["gameId", "playId", "totalDistanceTraveledByPossessionTeam"]
    ]
)
merged_data_reordered = combined_data_with_distance[columns_order]

# Exporting the file
output_file = "combined_data_with_positions_and_total.csv"
merged_data_reordered.to_csv(output_file, index=False)
