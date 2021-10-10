from results import graph, superscore, parse_link, download_yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("link", help="a link to a results page from duosmium.com")
parser.add_argument("module", help="which module to run ('superscore,' 'graph,' or 'download')")
parser.add_argument("--event", help="Provide an event if you want to create a graph of placements in a certain event")
parser.add_argument("--school", help="Provide a school if you want to create a graph of a certain school's placements")
args = parser.parse_args()

m = args.module
link = args.link

file, events, name = parse_link.parse(link)

if m == "superscore":
    scores = parse_link.superscore(file, link)
    superscore.main(scores, events, name)
    print(f"Superscored CSV can be found in ./csv_out/{name}")
elif m == "download":
    download_yaml.main(file, name, link)
elif m == "graph":
    scores = parse_link.superscore(file, link)
    if args.event:
        graph.event_graph(scores, args.event)
    elif args.school:
        graph.school_placements(scores, args.school)
    else:
        graph.overall(scores)
else:
    raise argparse.ArgumentTypeError("__main__.py: error: module must be 'superscore,' 'graph,' or 'download'")
