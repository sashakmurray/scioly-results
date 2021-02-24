import yaml


def get_dict(file_name):
    file = f"sciolyFF_files/{file_name}.yaml"
    with open(file) as fin:
        dictionary = yaml.safe_load(fin)
    return dictionary


def get_teams(file, sup):
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


def event_list(file):
    events = []
    for event in file["Events"]:
        # don't add trial events
        if len(event) == 1:
            events.append(event["name"])
    return events


def tournament_name(file):
    return file["Tournament"]["short name"]


def get_results(file, teams):
    events = event_list(file)

    num_teams = len(file["Teams"])
    results = {}
    for school in teams.values():
        results[school] = {}

    for item in file["Placings"]:
        # if the team number is one of the ones we are looking for,
        # it will be a key in the results dictionary
        if (e := item["event"]) in events:
            team = teams[item["team"]]
            if "Harriton" in team and e == "Experiment and Data Analysis":
                print(results[team])
            p = item.get("place", num_teams)
            if e in results[team]:
                results[team][e] = min(p, results[team][e])
            else:
                results[team][e] = p
    return results


def full_results(file):
    teams = get_teams(file, sup=False)
    return get_results(file, teams)


def get_superscore(file):
    teams = get_teams(file, sup=True)
    return get_results(file, teams)


if __name__ == "__main__":
    ggso = get_dict("ggso")
    print(get_superscore(ggso))
