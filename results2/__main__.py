from results2.sciolyFF import sciolyFF
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("link", help="a link to a results page from duosmium.com")
parser.add_argument("module", help="which module to run ('superscore,' 'graph,' 'histogram', or 'download')")
parser.add_argument("--event", help="Provide an event if you want to create a graph of placements in a certain event")
parser.add_argument("--school", help="Provide a school if you want to create a graph of a certain school's placements")
args = parser.parse_args()

m = args.module
link = args.link

file = sciolyFF(link)

if m == "superscore":
    file.write_superscore()
    print(f"Superscored CSV can be found in {file.get_path(superscore=True)}")
elif m == "download":
    file.download()
    print(f"YAML file can be found in {file.get_path(superscore=False)}")
else:
    raise argparse.ArgumentTypeError("__main__.py: error: module must be 'superscore' or 'download'")
