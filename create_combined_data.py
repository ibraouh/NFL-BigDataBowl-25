import pandas as pd

# importing all the files with the data
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


# Filtering the stats needed
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
        "playDescription",
    ]
]

# Merging data
merged_data = pd.merge(games_selected, plays_selected, on="gameId")
merged_data_sorted = merged_data.sort_values(by=["gameId", "playId"])
tracking_all_weeks = pd.concat(
    [week1, week2, week3, week4, week5, week6, week7, week8, week9], ignore_index=True
)

# Calculating the possesion
tracking_with_possession = pd.merge(
    tracking_all_weeks,
    merged_data_sorted[["gameId", "playId", "possessionTeam"]],
    on=["gameId", "playId"],
)

tracking_possession_team = tracking_with_possession[
    (tracking_with_possession["club"] == tracking_with_possession["possessionTeam"])
    & (tracking_with_possession["frameType"] == "BEFORE_SNAP")
]

total_distance_possession_team = (
    tracking_possession_team.groupby(["gameId", "playId"])["dis"]
    .sum()
    .reset_index()
    .rename(columns={"dis": "totalDistanceTraveledByPossessionTeam"})
)

combined_data_with_distance = pd.merge(
    merged_data_sorted,
    total_distance_possession_team,
    on=["gameId", "playId"],
    how="left",
)


# Reordering data for better visibility
columns_order = ["gameId", "playId", "totalDistanceTraveledByPossessionTeam"] + [
    col
    for col in merged_data_sorted.columns
    if col not in ["gameId", "playId", "totalDistanceTraveledByPossessionTeam"]
]
merged_data_reordered = combined_data_with_distance[columns_order]

# Exporting the file
output_file = "combined_data.csv"
merged_data_reordered.to_csv(output_file, index=False)
