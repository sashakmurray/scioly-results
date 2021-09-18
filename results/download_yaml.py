import yaml
import os


def download(file: dict, name: str) -> None:
    t = file["Tournament"]

    p = f"sciolyFF_files/{t['division']}/{t['year']}/{name}.yaml"
    directory = os.path.dirname(p)

    if not os.path.exists(directory):
        os.makedirs(directory)

    
    with open(p, "w+") as fout:
        #TODO: fix weird order thing?
        yaml.dump(file, fout, default_flow_style=False)
        #fout.write(f.content.decode("utf-8"))

def main(file: dict, name: str, link: str) -> None:
    if "duosmium" not in link:
        raise Exception("Link must be from www.duosmium.org")

    download(file, name)
