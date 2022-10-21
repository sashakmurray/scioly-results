import os
import csv

import yaml
import requests
import pandas as pd
import matplotlib.pyplot as plt


class sciolyFF:
    def __init__(self, link: str):
        file = "https://duosmium.org/data/{}.yaml".format(link.split("/")[-2])
        self.file = yaml.safe_load(requests.get(file).content)

        self.results = self.superscore()
        self.events = self.get_events()
        self.name = self.get_tournament_name()

    def download(self) -> None:
        path = self.get_path(superscore=False)
        directory = os.path.dirname(path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, "w+") as fout:
            # TODO: fix weird order thing?
            yaml.dump(self.file, fout, default_flow_style=False)

    def write_superscore(self) -> None:
        path = self.get_path(superscore=True)
        directory = os.path.dirname(path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, "w", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=["School"] + self.events + ["Total"]
            )
            writer.writeheader()

            for school in sorted(
                self.results, key=lambda x: sum(self.results[x].values())
            ):
                writer.writerow(
                    {"School": school}
                    | (self.results[school])
                    | {"Total": sum(self.results[school].values())}
                )

    def superscore(self) -> dict:
        t = self.teams(sup=True)
        return self.get_results(t)

    def teams(self, sup: bool) -> dict:
        teams = {}
        for team in self.file["Teams"]:
            t = f'{team["school"]} {team["state"]}'
            if sup:
                teams[team["number"]] = t
            else:
                try:
                    teams[team["number"]] = f'{t} {team["suffix"]}'
                except KeyError:
                    teams[team["number"]] = t
        return teams

    def get_results(self, teams: dict) -> dict:
        es: list = self.get_events()

        num_teams = len(self.file["Teams"])
        results = {}
        for school in teams.values():
            results[school] = {}

        for item in self.file["Placings"]:
            if (e := item["event"]) in es:
                team = teams[item["team"]]
                p = item.get("place", num_teams)
                if e in results[team]:
                    results[team][e] = min(p, results[team][e])
                else:
                    results[team][e] = p
        return results

    def get_events(self) -> list[str]:
        e = []
        for event in self.file["Events"]:
            # don't add trial events
            if "trial" not in event:
                e.append(event["name"])
        return e

    def get_tournament_name(self) -> str:
        tournament_info = self.file["Tournament"]

        if "short name" in tournament_info:
            name = tournament_info["short name"]
        elif "name" in tournament_info:
            name = tournament_info["name"]
        elif tournament_info["level"] == "States":
            name = f"{tournament_info['state']}_{tournament_info['level']}"
        else:
            name = tournament_info["level"]

        return name.replace(" ", "_")

    def get_teams(self, sup: bool) -> dict:
        teams = {}
        for team in self.file["Teams"]:
            t = f'{team["school"]} {team["state"]}'
            if sup:
                teams[team["number"]] = t
            else:
                try:
                    teams[team["number"]] = f'{t} {team["suffix"]}'
                except KeyError:
                    teams[team["number"]] = t
        return teams

    def get_path(self, superscore=True):
        t = self.file["Tournament"]
        if superscore:
            return f"superscores/{t['division']}/{t['year']}/{self.name}.csv"
        else:
            return f"sciolyFF_files/{t['division']}/{t['year']}/{self.name}.yaml"

