from . import scilympiad, sciolyFF


def parse(link: str) -> tuple:
    if "scilympiad" in link:
        soup = scilympiad.get_soup(link)
        file = scilympiad.get_scores(soup)
        events = scilympiad.get_events(soup)
        name = scilympiad.tournament_name(soup)
    else:
        file = sciolyFF.get_dict(link)
        events = sciolyFF.events(file)
        name = sciolyFF.tournament_name(file)

    return file, events, name

def superscore(file, link):
    if "scilympiad" in link:
        return scilympiad.superscore(file)
    # TODO: do this for scilympiad
    return sciolyFF.superscore(file)


def main(link):
    if "scilympiad" not in link and "duosmium" not in link:
        raise Exception("Link must be scilympiad or duosmium")

    return parse(link)
