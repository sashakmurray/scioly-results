import sqlite3

con = sqlite3.connect("results.db")

cur = con.cursor()

cur.execute(
    """CREATE TABLE tournaments (
            name TEXT NOT NULL PRIMARY KEY,
            num_teams INTEGER,
            quality REAL,
            top_teams INTEGER,
            score REAL
        )"""
)

con.commit()

con.close()
