import ezsheets
from scilympiad_scraper import *
import sciolyFF_parser


def write_placements(imp, ss):
    if "http" in imp:
        soup = get_soup(imp)
        scores = superscore(get_scores(soup))
        events = get_events(soup)
    else:
        file = sciolyFF_parser.get_dict(imp)
        scores = sciolyFF_parser.get_superscore(file)
        events = sciolyFF_parser.event_list(file)

    ss = ezsheets.Spreadsheet(ss)[0]

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
        "soaps",
        "1hPzt4RiXsR4i9vDmoR6XCD6eJ_tUXDlhJE6gU3qG4QU"
    )
