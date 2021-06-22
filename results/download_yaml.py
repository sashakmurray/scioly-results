import yaml
import requests
import os
from .sciolyFF import tournament_name


def download(link: str) -> None:
    file = "https://duosmium.org/data/{}.yaml".format
    f = requests.get(file(link[link.rfind("/"):]))
    dictionary = yaml.safe_load(f.content)
    t = dictionary["Tournament"]
    name = tournament_name(dictionary)

    p = f"sciolyFF_files/{t['division']}/{t['year']}/{name}.yaml"
    directory = os.path.dirname(p)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(p, "w+") as fout:
        fout.write(f.content.decode("utf-8"))

def main(link):
    download(link)
