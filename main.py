import requests
from bs4 import BeautifulSoup

def parse_animals(table):
    rows = table.find_all("tr")
    # Represent each row as list of <td/>
    rows = [r.find_all("td") for r in rows]
    # Remove rows without 7 <td/>
    rows = filter(lambda r: len(r)==7, rows)

    adjectives = dict()
    for row in rows:
        name=row[0].text.strip() if row[0].text else ""
        adjs = row[5].text.split(",") if row[5].text else []
        for adj in adjs:
            if not adjectives.get(adj):
                adjectives[adj] = [name]
            else:
                adjectives[adj] = adjectives[adj] + [name]
    
    return adjectives

def pretty_print_dict(d):
    for k in d.keys():
        print("{adj}:{animals}".format(adj=k, animals=d[k]))



def main():
    URL = "https://en.wikipedia.org/wiki/List_of_animal_names"
    page = requests.get(URL,timeout=3)

    soup = BeautifulSoup(page.content, "html.parser")

    # Sort by class_="wikitable sortable" since the last class "jquery..." is added in js, and bs doesn't support js
    tables = soup.find_all("table", class_="wikitable sortable")

    adjectives = dict()
    for table in tables:
        table_adjectives = parse_animals(table)
        adjectives.update(table_adjectives)


    pretty_print_dict(adjectives)
        

if __name__ == "__main__":
    main()