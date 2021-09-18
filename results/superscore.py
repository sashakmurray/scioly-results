import csv
import os

def write_placements(scores, events, name) -> None:
    path = f"csv_out/{name}.csv"
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["School"] + events + ["Total"])
        writer.writeheader()

        for school in sorted(scores, key=lambda x: sum(scores[x].values())):
            writer.writerow({"School": school} | (scores[school]) | {"Total": sum(scores[school].values())})

def main(scores, events, name):
    write_placements(scores, events, name)

