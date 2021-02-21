import ezsheets
from scilympiad_results import *
import sciolyFF_results


def write_placements(inp, ss):
    if "scilympiad" in inp:
        soup = get_soup(inp)
        scores = superscore(get_scores(soup))
        events = get_events(soup)
    else:
        file = sciolyFF_results.get_dict(inp)
        scores = sciolyFF_results.get_superscore(file)
        events = sciolyFF_results.event_list(file)

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
        "ggso",
        "18Mw8hzuGcCSzD3gZLhvXRK9Cal4PD-GO0kYF_ODTcpg"
    )
