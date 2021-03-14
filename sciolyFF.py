import yaml


def get_dict(file_name):
    file = f"sciolyFF_files/{file_name}.yaml"
    with open(file) as fin:
        dictionary = yaml.safe_load(fin)
    return dictionary


def teams(file, sup):
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


def events(file):
    e = []
    for event in file["Events"]:
        # don't add trial events
        if len(event) == 1:
            e.append(event["name"])
    return e


def tournament_name(file):
    return file["Tournament"]["short name"]


def get_medals(file):
    return file["Tournament"]["medals"]


def all_medals(file):
    m = {}
    num_medals = get_medals(file)
    for team, placements in superscore(file).items():
        m[team] = len([i for i in placements.values() if i <= num_medals])
    return m


def team_medals(file, team):
    m = get_medals(file)
    if c := superscore(file).get(team, None):
        return len(list(filter(lambda x: x <= m, c.values())))
    raise Exception("School did not compete. Try adding the state after the school name.")


def results(file, teams):
    es = events(file)

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


def full_results(file):
    t = teams(file, sup=False)
    return results(file, t)


def superscore(file):
    t = teams(file, sup=True)
    return results(file, t)


if __name__ == "__main__":
    soaps = get_dict("soaps")
    print(all_medals(soaps))
