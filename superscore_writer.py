import ezsheets
from scilympiad_scraper import *


def write_placements(URL, ss):
    soup = get_soup(URL)
    scores = superscore(get_scores(soup))
    ss = ezsheets.Spreadsheet(ss)[0]
    events = get_events(soup)

    rows = ss.getRows()
    rows[0] = ["School"] + list(events) + ["Team Score"]

    i = 1
    for school, p in scores.items():
        p = list(p.values())
        rows[i] = [school] + p + [sum(p)]
        i += 1

    points = len(rows[1]) - 1
    rankings = [rows[0]] + sorted(rows[1:i - 1], key=lambda x: x[points])
    p_loc = len(rows[0]) + 1
    placements = range(1, i - 1)

    ss.updateRows(rankings)
    ss.updateColumn(p_loc, ['Placement'] + list(placements))
    ss.refresh()


if __name__ == "__main__":
    write_placements(
        "https://scilympiad.com/solon/Info/Results/abdbcd4e-bab9-435c-abc0-4d84964c7bf6",
        "1jQEImnVjz7m26ycYSVWq_dOLIDRpTsCsQc6zGMytOTA"
    )
