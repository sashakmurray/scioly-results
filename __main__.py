from results import graph, scilympiad, sciolyFF, spreadsheet
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("-m", dest="module")
args = parser.parse_args()

m = args.module
link = args.file

file, events, name = parse_link.parse(link)
