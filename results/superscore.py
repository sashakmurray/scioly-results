import csv
import os

from . import scilympiad, sciolyFF


def write_placements(link) -> None:
    if "scilympiad" in link:
        soup = scilympiad.get_soup(link)
        scores = scilympiad.superscore(scilympiad.get_scores(soup))
        events = scilympiad.get_events(soup)
        name = scilympiad.tournament_name(soup)
    else:
        file = sciolyFF.get_dict(link)
        scores = sciolyFF.superscore(file)
        events = sciolyFF.events(file)
        name = sciolyFF.tournament_name(file)

    path = f"csv_out/{name}.csv"
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["School"] + events)
        writer.writeheader()

        for school in scores:
            writer.writerow({"School": school} | (scores[school]))

def main():
    write_placements("https://duosmium.org/results/2021-05-22_nationals_c")

if __name__ == "__main__":
    write_placements("https://duosmium.org/results/2021-05-22_nationals_c")
