import matplotlib.pyplot as plt
from scilympiad_scraper import *
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
    ax1.xaxis.set_ticks(range(0, len(scores) + 1, 10))

    ax2.plot(range(1, 11), list(scores.values())[:10])
    ax2.set_title("Scores for top 10 teams")
    ax2.set_xlabel("Placement")
    ax2.set_ylabel("Points")
    ax2.xaxis.set_ticks(range(1, 11, 1))

    mplcursors.cursor(ax1)
    plt.show()


def event_graph(data, event):
    fig, ax = plt.subplots()
    placements = {}
    for school, value in data.items():
        placements[school] = value[event]

    x_values = range(1, len(placements) + 1)
    y_values = placements.values()
    print(x_values)
    print(y_values)
    ax.scatter(x_values, y_values)
    plt.show()


if __name__ == "__main__":
    event_graph(
        get_scores(
            "https://scilympiad.com/solon/Info/Results/abdbcd4e-bab9-435c-abc0-4d84964c7bf6"
        ),
        "Designer Genes",
    )
