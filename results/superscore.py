import csv
import os

def write_placements(scores, events, name) -> None:
    path = f"csv_out/{name}.csv"
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["School"] + events)
        writer.writeheader()

        for school in scores:
            writer.writerow({"School": school} | (scores[school]))

def main(scores, events, name):
    write_placements(scores, events, name)

