import yaml
import requests
import os


def get_dict(link: str) -> dict:
    file = "https://duosmium.org/data/{}.yaml".format
    f = requests.get(file(link[link.rfind("/"):]))
    dictionary = yaml.safe_load(f.content)
    return dictionary


def download(link: str) -> None:
    file = "https://duosmium.org/data/{}.yaml".format
    f = requests.get(file(link[link.rfind("/"):]))
    dictionary = yaml.safe_load(f.content)
    name = ""
    t = dictionary["Tournament"]
    if "short name" in t:
        name = t["short name"]
    elif "name" in t:
        name = t["name"]
    elif t["level"] == "States":
        name = f"{t['state']}_{t['level']}"
    elif t["level"] == "Nationals":
        name = t["level"]
    else:
        name = link[link.rfind("/"):]

    p = f"sciolyFF_files/{t['division']}/{t['year']}/{name}.yaml"
    directory = os.path.dirname(p)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(p, "w+") as fout:
        fout.write(f.content.decode("utf-8"))


def teams(file: dict, sup: bool) -> dict:
    teams = {}
    for team in file["Teams"]:
        t = f'{team["school"]} {team["state"]}'
        if sup:
            teams[team["number"]] = t
        else:
            try:
                teams[team["number"]] = f'{t} {team["suffix"]}'
            except KeyError:
                teams[team["number"]] = t
    return teams


def events(file: dict) -> list[str]:
    e = []
    for event in file["Events"]:
        # don't add trial events
        if len(event) == 1:
            e.append(event["name"])
    return e


def tournament_name(file: dict) -> str:
    return file["Tournament"]["short name"]


def get_medals(file: dict) -> int:
    return file["Tournament"]["medals"]


def results(file: dict, teams: dict) -> dict:
    es: list = events(file)

    num_teams = len(file["Teams"])
    results = {}
    for school in teams.values():
        results[school] = {}

    for item in file["Placings"]:
        # if the team number is one of the ones we are looking for,
        # it will be a key in the results dictionary
        if (e := item["event"]) in es:
            team = teams[item["team"]]
            p = item.get("place", num_teams)
            if e in results[team]:
                results[team][e] = min(p, results[team][e])
            else:
                results[team][e] = p
    return results


def full_results(file: dict) -> dict:
    t = teams(file, sup=False)
    return results(file, t)


def superscore(file: dict) -> dict:
    t = teams(file, sup=True)
    return results(file, t)


def sorted_superscore(file: dict) -> list:
    scores = superscore(file)
    return sorted(scores.keys(), key=lambda x: sum(scores[x].values()))


def all_medals(file: dict) -> dict:
    m = {}
    num_medals: int = get_medals(file)
    sup: dict = superscore(file)
    for team in sorted_superscore(file):
        m[team] = len([p for p in sup[team].values() if p <= num_medals])
    return m


if __name__ == "__main__":
    download("https://duosmium.org/results/2021-05-22_nationals_c")
    nats = get_dict("https://duosmium.org/results/2021-05-22_nationals_c")

