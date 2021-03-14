import matplotlib.pyplot as plt
from scilympiad import *
import mplcursors


def points(data):
    res = {}
    for school, placements in data.items():
        res[school] = sum(placements.values())
    return {k: v for k, v in sorted(res.items(), key=lambda x: x[1])}


def overall(data):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
    scores = points(data)

    ax1.plot(range(1, len(scores) + 1), scores.values())
    ax1.set_title("Overall score distribution")
    ax1.set_xlabel("Placement")
    ax1.set_ylabel("Points")
    ax1.xaxis.set_ticks(range(0, len(scores) + 1, 15))

    ax2.plot(range(1, 11), list(scores.values())[:10])
    ax2.set_title("Scores for top 10 teams")
    ax2.set_xlabel("Placement")
    ax2.set_ylabel("Points")
    ax2.xaxis.set_ticks(range(1, 11, 1))

    mplcursors.cursor(ax1)
    plt.show()


def event_graph(data, event):
    fig, ax = plt.subplots()
    ax.set_title(f"Placements in {event}")

    placements = {}
    for school, value in data.items():
        placements[school] = value[event]

    x_values = range(1, len(placements) + 1)
    y_values = placements.values()

    ax.scatter(x_values, y_values)
    ax.set_xlabel("School placement")
    ax.set_ylabel("Placement in event")

    ax.xaxis.set_ticks(range(0, len(placements) + 1, 15))
    ax.yaxis.set_ticks(range(0, len(y_values) + 1, 15))
    plt.show()


def school_placements(data, school):
    fig, ax = plt.subplots()
    ax.set_title(f"{school}'s placements")

    events = list(data.values())[0].keys()

    placements = []
    teams = []
    for s in data:
        if school in s:
            placements.append(data[s])
            teams.append(s[s.rfind(" ") :])
    for team in placements:
        ax.scatter(events, team.values(), label=f"Team {teams[0]}")
        del teams[0]

    ax.set_ylabel("Placement")
    plt.xticks(range(len(events)), rotation=90)
    plt.tight_layout(rect=[0, 0, 0.95, 0.90])
    ax.legend()
    plt.show()


if __name__ == "__main__":
    school_placements(
        get_scores(
            get_soup(
                "https://scilympiad.com/mit/Info/Results/f7818bd3-00e8-466c-a1d0-fae5973a01cf"
            )
        ),
        "Lower Merion High School"
    )
