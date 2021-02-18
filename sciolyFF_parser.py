import yaml


def get_dict(file_name):
    file = f"sciolyFF_files/{file_name}.yaml"
    with open(file) as fin:
        dictionary = yaml.safe_load(fin)
    return dictionary


def get_teams(file, sup):
    teams = {}
    for team in file["Teams"]:
        if sup:
            teams[team["number"]] = team["school"]
        else:
            try:
                teams[team["number"]] = team["school"] + " " + team["suffix"]
            except KeyError:
                teams[team["number"]] = team["school"]
    return teams


def event_list(file):
    events = set()
    for event in file["Events"]:
        # don't add trial events
        if len(event) == 1:
            events.add(event["name"])
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
            if e in results[team] and "place" in item:
                results[team][e] = min(item["place"], results[team][e])
            else:
                try:
                    results[team][e] = item["place"]
                except KeyError:
                    # if the team did not participate in that event,
                    # a no-show is worth the max possible amount of points
                    results[team][e] = num_teams
    return results


def full_results(file):
    teams = get_teams(file, sup=False)
    return get_results(file, teams)


def get_superscore(file):
    teams = get_teams(file, sup=True)
    return get_results(file, teams)


soaps = get_dict("soaps")
print(get_superscore(soaps))
