import sqlite3

con = sqlite3.connect("results.db")
cur = con.cursor()

TOP_TEAMS = {"mason", "seven lakes", "troy", "solon", "acton boxborough", "west windsor-plainsboro south", "west windsor-plainsboro north", "mountain view", "enloe", "carmel", "stevenson", "northville", "new trier", "harriton", "marquette"}

# cur.execute(
#     """CREATE TABLE tournaments (
#         name TEXT NOT NULL PRIMARY KEY,
#         num_teams INTEGER,
#         quality REAL,
#         top_teams INTEGER,
#         score REAL
#     )"""
# )


def add_tournament(name: str, num_teams: int, quality: float):
    top_teams = 11  # use TOP_TEAMS and tourney results to determine number of top teams
    score = 0
    if num_teams / 10 > 10:
        score += 10
    else:
        score += num_teams / 10
    score += quality
    score += top_teams if top_teams < 10 else 10
    cur.execute(f"DELETE FROM tournaments WHERE name = ?", (name,))
    cur.execute(f"INSERT INTO tournaments VALUES (?, ?, ?, ?, ?)", (name, num_teams, quality, top_teams, score))


def get_tournament_score(name: str):
    for score in cur.execute(f"SELECT score FROM tournaments WHERE name = ?", (name,)):
        print(score)


add_tournament("Nationals 2022", 60, 6.0)
get_tournament_score("Nationals 2022")
con.commit()

con.close()
