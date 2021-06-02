import ezsheets
import scilympiad
import sciolyFF


def write_placements(inp, spreadsheet: str) -> None:
    if "scilympiad" in inp:
        soup = scilympiad.get_soup(inp)
        scores = scilympiad.superscore(scilympiad.get_scores(soup))
        events = scilympiad.get_events(soup)
    else:
        file = sciolyFF.get_dict(inp)
        scores = sciolyFF.superscore(file)
        events = sciolyFF.events(file)

    ss = ezsheets.Spreadsheet(spreadsheet)
    ss = ss[0]

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
        "https://scilympiad.com/soup/Info/Results/e570869b-2dda-4e41-b7fd-85e899ccbb1f",
        "1_oqZ2nwcS8XHQcPdyQbIJlwKCxCvaBz17sfAogYR4lA"
    )
