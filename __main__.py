from results import graph, superscore, parse_link, download_yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("-m", dest="module")
args = parser.parse_args()

m = args.module
link = args.file

file, events, name = parse_link.parse(link)

if m == "superscore":
    scores = parse_link.superscore(file, link)
    superscore.main(scores, events, name)
    print(f"Superscored CSV can be found in ./csv_out/{name}")
elif m == "download":
    download_yaml.main(file, name, link)
elif m == "graph":
    #TODO: do this :P
    pass
else:
    raise argparse.ArgumentTypeError("__main__.py: error: module must be 'superscore,' 'graph,' or 'spreadsheet'")
