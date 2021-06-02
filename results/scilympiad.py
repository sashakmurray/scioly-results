from bs4 import BeautifulSoup
import requests


def get_soup(URL: str):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_events(soup) -> list[str]:
    events = []
    top_row = soup.find_all("th")
    for event in top_row[3:]:
        event = event.text.strip()
        if "trial" not in event.lower():
            events.append(event)
    return events


def all_events(soup) -> list[str]:
    top_row = soup.find_all("th")
    events = [event.text.strip() for event in top_row[3:]]
    return events


def trials(soup) -> list[int]:
    events = []
    top_row = soup.find_all("th")
    for i, event in enumerate(top_row[3:]):
        event = event.text.strip()
        if "trial" in event.lower():
            events.append(i)
    return events


def get_scores(soup) -> dict:
    events = all_events(soup)

    data = {}
    schools = soup.find("tbody")
    for school in schools.find_all('tr')[:-1]:
        placements = {}
        school = school.find_all('td')
        for i in range(3, len(events) + 3):
            if 'trial' not in events[i - 3].lower():
                placements[events[i - 3]] = int(school[i].text.strip())
        data[school[0].text.strip()] = placements

    return data


def superscore(data: dict) -> dict:
    results = {}
    for school in data:
        if (c := ",") in school or (c := ".") in school:
            school_name = school[:school.rfind(c)]
            if school_name not in results:
                results[school_name] = data[school]
            else:
                for event in results[school_name]:
                    if data[school][event] < results[school_name][event]:
                        results[school_name][event] = data[school][event]
    return results


if __name__ == "__main__":
    # UT Austin
    s = get_soup("https://scilympiad.com/solon/Info/Results/abdbcd4e-bab9-435c-abc0-4d84964c7bf6")
    print(s)
